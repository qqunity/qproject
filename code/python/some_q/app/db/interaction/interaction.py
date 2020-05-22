from db.client.client import MySQLConnection
from db.exceptions import UserNotFoundException, UrlNotFoundException
from db.models.models import User, Base, MusicalComposition


class DbInteraction:

    def __init__(self, host, port, user, password, db_name, rebuild_db=False):
        self.mysql_connection = MySQLConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db
        )

        self.engine = self.mysql_connection.connection.engine

        if rebuild_db:
            self.create_table_users()
            self.create_table_musical_compositions()

    def create_table_users(self):
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['users'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS users')
            Base.metadata.tables['users'].create(self.engine)

    def create_table_musical_compositions(self):
        if not self.engine.dialect.has_table(self.engine, 'musical_compositions'):
            Base.metadata.tables['musical_compositions'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS musical_compositions')
            Base.metadata.tables['musical_compositions'].create(self.engine)

    def add_user_info(self, username, email, password):
        user = User(
            username=username,
            email=email,
            password=password
        )
        self.mysql_connection.session.add(user)
        return self.get_user_info(username)

    def del_user_info(self, username):
        if self.mysql_connection.session.query(User).filter_by(username=username).first():
            self.del_all_musical_compositions_info_by_username(username)
            self.mysql_connection.session.query(User).filter_by(username=username).delete()
        else:
            raise UserNotFoundException('User not found')

    def get_user_info(self, username):
        user = self.mysql_connection.session.query(User).filter_by(username=username).first()
        if user:
            self.mysql_connection.session.expire_all()
            return {'username': user.username, 'email': user.email, 'password': user.password, 'musical_compositions': self.get_all_musical_compositions_info_by_username(username)[username] if self.get_all_musical_compositions_info_by_username(username) else list()}
        else:
            raise UserNotFoundException('User not found')

    def edit_user_info(self, username,  new_username=None, new_email=None, new_password=None):
        user = self.mysql_connection.session.query(User).filter_by(username=username).first()
        if user:
            if new_username is not None:
                user.username = new_username
            if new_email is not None:
                user.email = new_email
            if new_password is not None:
                user.password = new_password
            return self.get_user_info(username)
        else:
            raise UserNotFoundException('User not found')

    def get_all_users_info(self):
        users = list(map(lambda user_info: user_info.username, self.mysql_connection.session.query(User).all()))
        users_info = dict()
        for user in users:
            users_info[user] = self.get_user_info(user)
        return users_info

    def add_musical_composition_info(self, username, url):
        user = self.mysql_connection.session.query(User).filter_by(username=username).first()
        if user:
            musical_comp = MusicalComposition(
                user_id=user.id,
                url=url
            )
            self.mysql_connection.session.add(musical_comp)
            return self.get_all_musical_compositions_info_by_username(username)
        else:
            raise UserNotFoundException('User not found')

    def get_all_musical_compositions_info_by_username(self, username):
        user = self.mysql_connection.session.query(User).filter_by(username=username).first()
        if user:
            musical_comps = self.mysql_connection.session.query(MusicalComposition).filter_by(user_id=user.id).all()
            self.mysql_connection.session.expire_all()
            musical_comps_info = dict()
            for musical_comp in musical_comps:
                if musical_comp.user.username in musical_comps_info:
                    musical_comps_info[musical_comp.user.username].append(musical_comp.url)
                else:
                    musical_comps_info[musical_comp.user.username] = list()
                    musical_comps_info[musical_comp.user.username].append(musical_comp.url)
            return musical_comps_info
        else:
            raise UserNotFoundException('User not found')

    def del_all_musical_compositions_info_by_username(self, username):
        user = self.mysql_connection.session.query(User).filter_by(username=username).first()
        if user:
            self.mysql_connection.session.query(MusicalComposition).filter_by(user_id=user.id).delete()
        else:
            raise UserNotFoundException('User not found')

    def edit_musical_composition_info_by_url(self, url, new_url=None, new_username=None):
        musical_comps = self.mysql_connection.session.query(MusicalComposition).filter_by(url=url).all()
        if musical_comps:
            if new_username is not None:
                user = self.mysql_connection.session.query(User).filter_by(username=new_username).first()
                if not user:
                    raise UserNotFoundException('User not found')
            for musical_comp in musical_comps:
                if new_username is not None:
                    musical_comp.user_id = user.id
                if new_url is not None:
                    musical_comp.url = new_url
                username = musical_comp.user.username
            return self.get_all_musical_compositions_info_by_username(username)
        else:
            raise UrlNotFoundException('Musical compositions not fount')

from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, UniqueConstraint, SMALLINT, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(VARCHAR(50), nullable=True)
    password = Column(VARCHAR(300), nullable=False)
    email = Column(VARCHAR(70), nullable=False)

    UniqueConstraint(username, name='username')
    UniqueConstraint(email, name='email')

    def __repr__(self):
        return f"<User(" \
               f"id='{self.id}'," \
               f"username='{self.username}'," \
               f"password='{self.password}'," \
               f"email='{self.email}'" \
               f")>"


class MusicalComposition(Base):
    __tablename__ = 'musical_compositions'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.{User.id.name}'), nullable=False)
    url = Column(VARCHAR(60), nullable=True)
    user = relationship('User', backref='musical_composition')

    def __repr__(self):
        return f"<MusicalComposition(" \
               f"id='{self.id}'," \
               f"user_id='{self.user.id}'," \
               f"url='{self.url}'" \
               f")>"

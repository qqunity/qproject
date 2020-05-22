import threading
import requests
import argparse

from flask import Flask, abort, request, jsonify

from app.api.utils import config_parser
from db.exceptions import UserNotFoundException, UrlNotFoundException
from db.interaction.interaction import DbInteraction


class Server:

    def __init__(self, host, port, db_host, db_port, db_user, db_password, db_name):
        self.host = host
        self.port = port

        self.db_interaction = DbInteraction(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db_name=db_name,
            rebuild_db=True
        )

        self.app = Flask(__name__)
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/data', view_func=self.get_data)
        self.app.add_url_rule('/add_user_info', view_func=self.add_user_info, methods=['POST'])
        self.app.add_url_rule('/get_user_info/<username>', view_func=self.get_user_info)
        self.app.add_url_rule('/del_user_info/<username>', view_func=self.del_user_info, methods=['DELETE'])
        self.app.add_url_rule('/edit_user_info/<username>', view_func=self.edit_user_info, methods=['PUT'])
        self.app.add_url_rule('/add_musical_composition_info', view_func=self.add_musical_composition_info, methods=['POST'])
        self.app.add_url_rule('/del_musical_compositions_info/<username>', view_func=self.del_all_musical_compositions_info_by_username, methods=['DELETE'])
        self.app.add_url_rule('/edit_musical_composition_info/<url>', view_func=self.edit_musical_composition_info_by_url, methods=['PUT'])

        self.app.register_error_handler(404, self.page_not_found)

    def page_not_found(self, err_description):
        return jsonify(error=str(err_description)), 404

    def run_server(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server

    def shutdown_server(self):
        requests.get(f'http://{self.host}:{self.port}/shutdown')

    def shutdown(self):
        terminate_func = request.environ.get('werkzeug.server.shutdown')
        if terminate_func:
            terminate_func()

    def get_home(self):
        return 'Hello, api server!'

    def get_data(self):
        data = self.db_interaction.get_all_users_info()
        if data:
            return data, 200
        else:
            abort(404, description='Data not found')

    def add_user_info(self):
        request_body = dict(request.json)
        username = request_body['username']
        password = request_body['password']
        email = request_body['email']
        self.db_interaction.add_user_info(
            username=username,
            password=password,
            email=email
        )
        return f'Success added {username}', 201

    def get_user_info(self, username):
        try:
            user_info = self.db_interaction.get_user_info(username)
            return user_info, 200
        except UserNotFoundException:
            abort(404, description='User not found')

    def del_user_info(self, username):
        try:
            self.db_interaction.del_user_info(username)
            return '', 204
        except UserNotFoundException:
            abort(404, description='User not found')

    def edit_user_info(self, username):
        request_body = dict(request.json)
        new_username = request_body['username']
        new_password = request_body['password']
        new_email = request_body['email']
        try:
            self.db_interaction.edit_user_info(
                username=username,
                new_username=new_username,
                new_password=new_password,
                new_email=new_email
            )
            return f'Success edited {username}', 200
        except UserNotFoundException:
            abort(404, description='User not found')

    def add_musical_composition_info(self):
        request_body = dict(request.json)
        username = request_body['username']
        url = request_body['url']
        self.db_interaction.add_musical_composition_info(
            username=username,
            url=url
        )
        return f'Success added musical composition for {username}', 201

    def del_all_musical_compositions_info_by_username(self, username):
        try:
            self.db_interaction.del_all_musical_compositions_info_by_username(username)
            return '', 204
        except UserNotFoundException:
            abort(404, description='User not found')

    def edit_musical_composition_info_by_url(self, url):
        try:
            request_body = dict(request.json)
            new_url = request_body['url']
            new_username = request_body['username']
            self.db_interaction.edit_musical_composition_info_by_url(
                url=url,
                new_url=new_url,
                new_username=new_username
            )
            return f'Success edited musical composition by url: {url}', 200
        except UrlNotFoundException:
            abort(404, description='Musical composition url not found')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, dest='config')

    args = parser.parse_args()

    config = config_parser(args.config)

    server_host = config['SERVER_HOST']
    server_port = config['SERVER_PORT']

    db_host = config['DB_HOST']
    db_port = config['DB_PORT']
    db_user = config['DB_USER']
    db_password = config['DB_PASSWORD']
    db_name = config['DB_NAME']

    server = Server(
        host=server_host,
        port=server_port,
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_password=db_password,
        db_name=db_name
    )
    server.run_server()

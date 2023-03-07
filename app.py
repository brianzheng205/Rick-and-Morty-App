import os
import requests
import ramapi
from ramapi import *

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # API
    # r = ramapi.requests.get('https://rickandmortyapi.com/api/location/20')
    JSON_locations = ramapi.Location.get_all() # JSON data of all locations
    locations = JSON_locations['results']

    for location in locations:
        del location['created']
        del location['dimension']
        del location['id']
        del location['url']

        # for i in range(len(location['residents'])):
        #     resident_url = location['residents'][i]
        #     start = resident_url.index('/', -4)
        #     resident_id = int(resident_url[start + 1:])
        #     # print(ramapi.Character.get(resident_id)['image'])
        #     location['residents'][i] = ramapi.Character.get(resident_id)['image']

    # a simple page that says hello
    @app.route('/')
    def hello():
        return locations

    return app
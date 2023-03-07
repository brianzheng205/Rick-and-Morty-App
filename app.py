import os
import requests
import ramapi
from flask import Flask, render_template


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
    # r = ramapi.requests.get('https://rickandmortyapi.com/api/character/avatar/612.jpeg')
    # print(r)
    JSON_locations = ramapi.Location.get_all() # JSON data of all locations
    locations = JSON_locations['results']

    for location in locations:
        # delete unncessary information
        del location['created']
        del location['dimension']
        del location['id']
        del location['url']

        # convert resident url to resident image url for rendering later
        for i in range(len(location['residents'])):
            resident_url = location['residents'][i]
            split = resident_url.index('/', -4)
            beginning_url = resident_url[:split + 1]
            resident_id = resident_url[split + 1:]
            image_url = beginning_url + 'avatar/' + resident_id + '.jpeg'
            location['residents'][i] = image_url
    
    # print(locations)

    @app.route('/')
    def convert():
        # return locations
        return render_template('app.html', locations = locations)

    return app
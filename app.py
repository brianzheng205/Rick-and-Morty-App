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
    # word = 'Hello World!'
    # r = requests.get('https://httpbin.org/get', params=word)
    # hi = {'hello': 'world'}
    # r = requests.post('https://jsonplaceholder.typicode.com/posts', params=hi)
    # print(r.text)
    # print(r.url)
    JSON_locations = ramapi.Location.get_all() # JSON data of all locations
    locations = JSON_locations['results']
    id_to_name_and_status = {}
    
    for i in range(1, 43):
        for character in ramapi.Character.get_page(i)['results']:
            id_to_name_and_status[character['id']] = [character['name'], character['status']]

    for location in locations:
        # delete unncessary information
        del location['created']
        del location['dimension']
        del location['id']
        del location['url']

        # convert resident url to [name, status, resident image url] for rendering later
        for i in range(len(location['residents'])):
            resident_url = location['residents'][i]
            split = resident_url.index('/', -4)
            beginning_url = resident_url[:split + 1]
            resident_id = resident_url[split + 1:]
            image_url = beginning_url + 'avatar/' + resident_id + '.jpeg'
            name, status = id_to_name_and_status[int(resident_id)]
            location['residents'][i] = [name, status, image_url]

    @app.route('/')
    def convert():
        # render website
        return render_template('app.html', locations = locations)

    return app
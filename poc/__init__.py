import json
import os

from flask import Flask, render_template, request, jsonify

from .calculator import get_frequency, INTONATION_NAME_MAP, ALL_NOTES
from .shortcuts import INDEX_MAP, get_ui_shortcuts_data, MOD_KEY_MAP

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # calculator tests
    @app.route('/calc', methods=['POST', 'GET'])
    def calc():
        if request.method == 'GET':
            return render_template(
                'calc.html',
                freq=-1,
                base_freq=440.0,
                note='A4',
                all_notes=ALL_NOTES,
                all_intonations=INTONATION_NAME_MAP
            )
        elif request.method == 'POST':
            return render_template(
                'calc.html',
                freq="{:.2f}".format(
                    calculator.get_frequency(
                        request.form['note'],
                        request.form['base_freq'],
                        request.form['intonation']
                    )
                ),
                note=request.form['note'],
                base_freq=request.form['base_freq'],
                intonation=INTONATION_NAME_MAP[request.form['intonation']],
                all_notes=ALL_NOTES,
                all_intonations=INTONATION_NAME_MAP
            )

    @app.route('/data/sc_index.json')
    def sc_index():
        return jsonify(INDEX_MAP)

    @app.route('/search', methods=['GET'])
    def search():
        return render_template(
            'search.html',
            shortcuts=get_ui_shortcuts_data(),
            mod_key_map=MOD_KEY_MAP
        )

    return app


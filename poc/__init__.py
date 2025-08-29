import json
import os

from flask import Flask, render_template, request, jsonify, redirect, url_for

from .calculator import get_frequency, get_note_durations, INTONATION_NAME_MAP, ALL_NOTES
from .shortcuts import get_ui_shortcuts_data, INDEX_MAP, MOD_KEY_MAP, UI_SC_DATA

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

    @app.route('/')
    def index():
        return render_template('index.html')

    # note to freq calculator
    @app.route('/calc')
    def calc():
        return redirect(url_for('note2freq'))

    @app.route('/note2freq', methods=['POST', 'GET'])
    def note2freq():
        if request.method == 'GET':
            return render_template(
                'note2freq.html',
                freq=-1,
                base_freq=440.0,
                note='A4',
                all_notes=ALL_NOTES,
                all_intonations=INTONATION_NAME_MAP
            )
        elif request.method == 'POST':
            return render_template(
                'note2freq.html',
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

    # bpm to note duration calculator
    @app.route('/beatduration', methods=['POST', 'GET'])
    def beatduration():
        if request.method == 'GET':
            return render_template(
                'beatduration.html',
                notes=None,
                sig_base=4,
                bpm=120,
            )
        elif request.method == 'POST':
            sig_base = int(request.form['sig_base'])
            bpm = float(request.form['bpm'])
            return render_template(
                'beatduration.html',
                notes=get_note_durations(sig_base, bpm),
                sig_base=sig_base,
                bpm=bpm,
            )

    # shortcut search
    @app.route('/data/sc_index.json')
    def sc_index():
        return jsonify(INDEX_MAP)

    @app.route('/search', methods=['GET'])
    def search():
        return render_template(
            'search.html',
            shortcuts=UI_SC_DATA,
            mod_key_map=MOD_KEY_MAP
        )

    return app


poc = create_app()

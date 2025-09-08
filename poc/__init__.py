import json
import os

from flask import Flask, render_template, request, jsonify, redirect, url_for
from jinja2 import Environment, FileSystemLoader

from .calculator import get_frequency, get_note_durations, get_all_notes, INTONATION_NAME_MAP
from .shortcuts import get_ui_shortcuts_data, INDEX_MAP, MOD_KEY_MAP, UI_SC_DATA
from .page_defaults import PageDefaults as PD


ALL_NOTES = get_all_notes()


def render_bespoke_templates():
    """
    Render templates that are considered static files by Flask and write files.
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    bespoke_template_dir = f'{base_dir}/bespoke_templates'
    templates = [
        {
            'path': 'static/css/main.css',
            'context': {'defaults': PD('static/css/main.css').css}
        }
    ]

    env = Environment(loader=FileSystemLoader(bespoke_template_dir))
    for template in templates:
        loaded_tmpl = env.get_template(template['path'])
        result = loaded_tmpl.render(template['context'])
        with open(os.path.join(base_dir, template['path']), 'w') as f:
            f.write(result)


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

    # Initialise page defaults
    index_pd = PD('index.html')
    search_pd = PD('search.html')
    note2Hz_pd = PD('note2Hz.html')
    note2ms_pd = PD('note2ms.html')

    # bespoke templates are not part of Flask
    render_bespoke_templates()

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
        return redirect(url_for('note2Hz'))

    @app.route('/note2freq')
    def note2freq():
        return redirect(url_for('note2Hz'))

    @app.route('/note2Hz', methods=['POST', 'GET'])
    def note2Hz():
        if request.method == 'GET':
            return render_template(
                'note2Hz.html',
                freq=-1,
                base_freq=440.0,
                note='A4',
                all_notes=ALL_NOTES,
                all_intonations=INTONATION_NAME_MAP
            )
        elif request.method == 'POST':
            return render_template(
                'note2Hz.html',
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
    @app.route('/beatduration')
    def beatduration():
        return redirect(url_for('note2ms'))

    @app.route('/note2ms', methods=['POST', 'GET'])
    def note2ms():
        if request.method == 'GET':
            return render_template(
                note2ms_pd.filename,
                notes=None,
                sig_base=4,
                bpm=120,
                page_data=note2ms_pd
            )
        elif request.method == 'POST':
            sig_base = int(request.form['sig_base'])
            bpm = float(request.form['bpm'])
            bpm = int(bpm) if bpm.is_integer() else bpm
            return render_template(
                note2ms_pd.filename,
                notes=get_note_durations(sig_base, bpm),
                sig_base=sig_base,
                bpm=bpm,
                page_data=note2ms_pd
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

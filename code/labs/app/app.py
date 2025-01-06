import os
import json
from flask import Flask, render_template, jsonify, request
import sys
sys.path.append(r'./..')

import configuration.main as configuration
import logging_setup.main as logging_setup


DEFAULT_CONFIG_FILE = "../../config.yaml"
config = configuration.load_config(DEFAULT_CONFIG_FILE)
CHECKPOINTS_DIR = f"../{config['DEFAULT_CHECKPOINT_DIR']}_extraction"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Return the list of .json files for the multi-select
@app.route('/api/list_files', methods=['GET'])
def list_files():
    data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), CHECKPOINTS_DIR)
    )
    files = [f for f in os.listdir(data_path) if f.endswith('.json')]
    return jsonify(files)

# Endpoint for reading a single file, used for the “first selected” file
@app.route('/api/single_document', methods=['GET'])
def single_document():
    """
    Usage: /api/single_document?filename=somefile.json
    Returns the JSON of that file, or [] if not found.
    """
    data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), CHECKPOINTS_DIR)
    )
    filename = request.args.get('filename')
    if not filename:
        return jsonify([])

    full = os.path.join(data_path, filename)
    if not os.path.isfile(full):
        return jsonify([])
    with open(full, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    return jsonify(data)

# Endpoint for reading multiple files in parallel for comparison
@app.route('/api/multiple_documents', methods=['POST'])
def multiple_documents():
    """
    Expects JSON like {"files": ["docA.json","docB.json"]}
    Returns { "docA.json": {...}, "docB.json": {...}, ... }
    """
    data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), CHECKPOINTS_DIR)
    )
    payload = request.json
    selected_files = payload.get('files', [])
    out = {}
    for f in selected_files:
        full = os.path.join(data_path, f)
        if os.path.isfile(full):
            with open(full, 'r', encoding='utf-8') as fp:
                out[f] = json.load(fp)
        else:
            out[f] = {}
    return jsonify(out)

if __name__ == '__main__':
    app.run(debug=True)
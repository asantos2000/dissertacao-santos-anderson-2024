from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Load the JSON data
DATA_FILE = './data/documents-2024-11-01-3.json'

def load_documents():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/documents')
def get_documents():
    documents = load_documents()
    return jsonify(documents)

if __name__ == '__main__':
    app.run(debug=True)

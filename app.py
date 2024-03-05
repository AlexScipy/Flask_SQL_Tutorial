from flask import Flask, request, jsonify
from utils_db import *

app = Flask(__name__)

@app.route('/insert_data', methods=['POST'])
def insert_data_route():
    data = request.get_json()
    table_name = data.get('table_name')
    if not table_name:
        return jsonify({'error': 'table_name is required'}), 400
    insert_data(table_name, data)
    return jsonify({'message': 'data inserted'}), 201

@app.route('/read_table_as_json', methods=['GET'])
def read_table_as_json_route():
    table_name = request.args.get('table_name')
    id = request.args.get('id')
    if not table_name:
        return jsonify({'error': 'table_name is required'}), 400
    json_data = read_table_as_json(table_name, id)
    if isinstance(json_data, dict):
        return json_data
    else:
        return jsonify(json_data), 200, {'Content-Type': 'application/json'}

@app.route('/read_data_by_name', methods=['GET'])
def read_data_by_name_route():
    table_name = request.args.get('table_name')
    name = request.args.get('name')
    if not table_name or not name:
        return jsonify({'error': 'table_name and name are required'}), 400
    data = read_data_by_name(table_name, name)
    return jsonify(data), 200

@app.route('/read_data_by_id', methods=['GET'])
def read_data_by_id_route():
    table_name = request.args.get('table_name')
    id = request.args.get('id')
    if not table_name or not id:
        return jsonify({'error': 'table_name and id are required'}), 400
    data = read_data_by_id(table_name, id)
    return jsonify(data), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    # Quando si interrompe l'esecuzione del programma, si chiude la connessione al database
    close_db()
    app.teardown_appcontext(close_db)
import sqlite3
import json


DATABASE = 'users.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = get_db()
    db.close()

def init_db():
    with get_db() as db:
        try:
            db.execute('''
                CREATE TABLE IF NOT EXISTS tabella_1 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value TEXT NOT NULL
                )
            ''')
            db.commit()
            print('Database e tabella creati correttamente')
        except Exception as e:
            print('Errore durante la creazione del database o della tabella:', e)


def insert_data(table_name, data):
    with get_db() as db:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(f':{key}' for key in data.keys())
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        try:
            db.cursor().execute(query, data)
            db.commit()
            print(f'Inseriti i dati in {table_name}')
        except Exception as e:
            print(f'Errore durante l\'inserimento dei dati in {table_name}:', e)

def read_data_by_name(table_name, name):
    with get_db() as db:
        query = f'SELECT * FROM {table_name} WHERE name=?'
        try:
            data = db.cursor().execute(query, (name,)).fetchall()
            print(f'Letti i dati da {table_name} con name={name}')
            return data
        except Exception as e:
            print(f'Errore durante la lettura dei dati da {table_name} con name={name}:', e)

def read_data_by_id(table_name, id):
    with get_db() as db:
        query = f'SELECT * FROM {table_name} WHERE id=?'
        try:
            data = db.cursor().execute(query, (id,))#.fetchall()
            columns = [description[0] for description in data.description]
            data = [dict(zip(columns, row)) for row in data.fetchall()]
            print(f'Letti i dati da {table_name} con id={id}')
            return data
        except Exception as e:
            print(f'Errore durante la lettura dei dati da {table_name} con id={id}:', e)

def read_table_as_json(table_name, id=None, name=None):
    with get_db() as db:
        if id is None and name is None:
            query = f'SELECT * FROM {table_name}'
        elif id is not None and name is None:
            query = f'SELECT * FROM {table_name} WHERE id=?'
        elif id is None and name is not None:
            query = f'SELECT * FROM {table_name} WHERE name=?'
        else:
            query = f'SELECT * FROM {table_name} WHERE id=? AND name=?'
        try:
            data = db.cursor().execute(query, (id,) if id else ()).fetchall()
            columns = [description[0] for description in db.cursor().description]
            json_data = [dict(zip(columns, row)) for row in data]
            print('JSON data:', json_data)
            json_data_str = json.dumps(json_data, indent=4)
            print('JSON:', json_data_str)
            return json_data_str
        except Exception as e:
            print(f'Errore durante la conversione dei dati in JSON:', e)
            return {'error': 'Errore durante la conversione dei dati in JSON'}, 500
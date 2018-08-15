'''
from flask import Flask
from flask_pymongo import PyMongo
import mongoDBLink

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'admin'
app.config['MONGO_URI'] = DB_USER['admin']
mongo = PyMongo(app)

@app.route('/')
def index():
    return 'home page'

if __name__ == "__main__":
    app.run(debug = True)
'''

from flask import current_app, g
from flask_pymongo import PyMongo
import mongoDBLink


def get_db():
    if 'db' not in g:
        current_app.config['MONGO_DBNAME'] = 'admin'
        current_app.config['MONGO_URI'] = DB_USER['admin']
        mongo = PyMongo(current_app)
        g.db = mongo.db
    return g.db

def close_db(e = None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

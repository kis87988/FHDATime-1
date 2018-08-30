
from flask import Flask,current_app
from flask_pymongo import PyMongo,pymongo
from MongoDBKey import *

'''
Please create a file all MongoDBkey contain the following:
AUTH:dict = {
    "HOST": 'mongodb://USERID:PASSWORD@HOST/DBName',
}
'''
class FHDAConnect():
    def __init__(self):
        try:
            self.app = Flask(__name__)
            self.app.config['MONGO_URI'] = AUTH["HOST"]
            self.mongo = PyMongo(self.app)
        except pymongo.errors.PyMongoError as e:
            print(str(e))
    def getMongo(self):
        return self.mongo
    def getApp(self):
        return self.app
'''
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
'''
from flask import Flask
from connectMongoDB import FHDAConnect
from flask_pymongo import PyMongo,pymongo

fhdaConnect = FHDAConnect()
app = fhdaConnect.getApp()

@app.route('/')
def index():
    try:
        print(fhdaConnect.getMongo().db.users.find({}))
        for elem in fhdaConnect.getMongo().db.users.find({}):
            print(elem)
    except pymongo.errors.PyMongoError as e:
        print(str(e))
    return "hi"

if __name__ == "__main__":
    app.run(debug = True)

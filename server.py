from flask import Flask
import json

app = Flask(__name__)
a = "Hello World!"


@app.route("/")
def listData():
	return getFile("DataSets.json")

def getFile(filename):
	f = open(filename, 'r')
	return f.read()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
from flask import Flask
import json

app = Flask(__name__)
app.debug = True

@app.route("/DataSets")
def datasets():
	return getFile("DataSets.json")

@app.route("/DataSets/<key>")
def datasetsByKey(key):
	js = json.loads(getFile("DataSets.json"))
	if key in js:
		result = {str(key): js[key]}
		return json.dumps(result)
	else:
		return "Error: Invalid Key {}".format(key)

@app.route("/data/<dataset>/<country>/<year>")
def getDatasetCountryYear(dataset, country, year):
	return getFile("{}/{}/{}.json".format(dataset, country, year))

@app.route("/data/<dataset>/<country>")
def getDatasetCountry(dataset, country):
	data = {dataset:[]}
	js = json.loads(getFile("%s.json" % dataset))
	for year in js['Years']:
		data[dataset].append(json.loads(getFile("{}/{}/{}.json".format(dataset, country, year))))
	
	return json.dumps(data)

@app.route("/DataSet/<dataset>")
def getDatasetInfo(dataset):
	return getFile("%s.json" % dataset)

@app.route("/DataSet/<dataset>/<key>")
def getDatasetInfoByKey(dataset, key):
	js = json.loads(getFile("%s.json" % dataset))
	if key in js:
		return json.dumps({key: js[key]})
	else:
		return "Error! Invalid Key or Dataset!"

def getFile(filename):
	return open(filename, 'r').read()

if __name__ == "__main__":
	app.run(port=80)
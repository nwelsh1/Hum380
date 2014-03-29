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

@app.route("/data")
def getAllData():
	data = {}
	dataSets = json.loads(getFile("DataSets.json"))
	for dataSet in dataSets['DataSets']:
		dataSetInfo = json.loads(getFile("%s.json" % dataSet))
		for country in dataSetInfo["Countries"]:
			for year in dataSetInfo["Years"]:
				print("{}/{}/{}.json".format(dataSet, country, year))
				js = json.loads(getFile("{}/{}/{}.json".format(dataSet, country, year)))
				if (dataSet not in data):
					data[dataSet] = {}
				if (country not in data[dataSet]):
					data[dataSet][country] = {}
				data[dataSet][country][year] = {"Percent": js['Percent']}
	return json.dumps(data)


def getFile(filename):
	return open(filename, 'r').read()

if __name__ == "__main__":
	app.run(port=80)
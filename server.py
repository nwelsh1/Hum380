from flask import Flask, render_template, url_for
import json, bisect

app = Flask(__name__)

@app.route("/DataSets")
def datasets():
	return getFile("DataSets.json")

@app.route("/data/<dataset>/<country>/<year>")
def getDatasetCountryYear(dataset, country, year):
	return getFile("{}/{}/{}.json".format(dataset, country, year))

@app.route("/dataByYear/<year>/<country>")
def getDataByYearCountry(year, country):
	data = {}
	dataSets = json.loads(getFile("DataSets.json"))
	for dataSet in dataSets['DataSets']:
		dataSetInfo = json.loads(getFile("%s.json" % dataSet))
		js = json.loads(getFile("{}/{}/{}.json".format(dataSet, country, year)))
		if (dataSet not in data):
			data[dataSet] = {}
		if (country not in data[dataSet]):
			data[dataSet][country] = {}
		data[dataSet][country][year] = {"Percent": js['Percent']}
	return json.dumps(data)

@app.route("/dataByYear/<year>")
def getDataByYear(year):
	data = {}
	dataSets = json.loads(getFile("DataSets.json"))
	for dataSet in dataSets['DataSets']:
		dataSetInfo = json.loads(getFile("%s.json" % dataSet))
		for country in dataSetInfo["Countries"]:
			js = json.loads(getFile("{}/{}/{}.json".format(dataSet, country, year)))
			if (dataSet not in data):
				data[dataSet] = {}
			if (country not in data[dataSet]):
				data[dataSet][country] = {}
			data[dataSet][country] = js['Percent']
	return json.dumps(data)

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

@app.route("/data/<dataset>")
def getDataBySet(dataset):
	data = {}
	dataSetInfo = json.loads(getFile("%s.json" % dataset))
	for country in dataSetInfo["Countries"]:
		for year in dataSetInfo["Years"]:
			js = json.loads(getFile("{}/{}/{}.json".format(dataset, country, year)))
			if country not in data:
				data[country] = {}
			data[country][year] = js["Percent"]
	return json.dumps(data)

@app.route("/data")
def getAllData():
	data = {}
	dataSets = json.loads(getFile("DataSets.json"))
	for dataSet in dataSets['DataSets']:
		dataSetInfo = json.loads(getFile("%s.json" % dataSet))
		for country in dataSetInfo["Countries"]:
			for year in dataSetInfo["Years"]:
				js = json.loads(getFile("{}/{}/{}.json".format(dataSet, country, year)))
				if (dataSet not in data):
					data[dataSet] = {}
				if (country not in data[dataSet]):
					data[dataSet][country] = {}
				data[dataSet][country][year] = {"Percent": js['Percent']}
	return json.dumps(data)

@app.route("/dataview/<dataset>")
def dataview(dataset):
    return render_template('dataview.html', pagetitle=dataset, style=url_for('static', filename="main.css"))

@app.route("/viewbyyear/<datasetname>")
def viewByYear(datasetname):
    dataset = json.loads(getDataBySet(datasetname))
    years = []
    byyear = {}
    for country in dataset:
        for year in dataset[country]:
            if year not in years:
                bisect.insort(years, year)
            if year not in byyear:
                byyear[year] = []
            byyear[year].append({ "country" : country, "value" : dataset[country][year] })
    
    return render_template('databyyear.html', years=years, byyear=byyear, style=url_for('static', filename="main.css"), pagetitle=datasetname + " by Year")

@app.route("/viewbycountry/<datasetname>")
def viewByCountry(datasetname):
    dataset = json.loads(getDataBySet(datasetname))
    countries = []
    bycountry = {}
    
    for country in dataset:
        for year in dataset[country]:
            if country not in countries:
                countries.append(country)
            if country not in bycountry:
                bycountry[country] = []
            bycountry[country].append({ "year" : year, "value" : dataset[country][year] })
    
    return render_template('databycountry.html', countries=countries, bycountry=bycountry, style=url_for('static', filename="main.css"), pagetitle=datasetname + " by Country")

@app.route("/")
def index():
    dataset_names = json.loads(getFile('DataSets.json'))['DataSets']
    datasets = []
    for dataset in dataset_names:
        with open(dataset + '.json', 'r') as f:
            datasets.append(json.loads(f.read()))
    return render_template('index.html', datasets=datasets,
        pagetitle='Data Viewer', style=url_for('static', filename="main.css"))

def getFile(filename):
	return open(filename, 'r').read()

if __name__ == "__main__":
	app.run(debug=True, port=80)
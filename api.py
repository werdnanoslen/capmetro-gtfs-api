from flask import Flask, request
from flask_restful import Resource, Api
import csv
import glob
import os

app = Flask(__name__)
api = Api(app)

fpattern = "capmetro_gtfs/*.txt"
files = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob(fpattern)]

class meta(Resource):
    def get(self):
        return files

class endpoint(Resource):
    def get(self, endpoint):
        if (endpoint in files):
            filename = 'capmetro_gtfs/' + endpoint + '.txt'
            file = open(filename, 'rb')
            reader = csv.reader(file)
            for row in reader:
                return row
        else:
            return meta().get()

class getRow(Resource):
    def get(self, endpoint, field, value):
        if (endpoint in files):
            filename = 'capmetro_gtfs/' + endpoint + '.txt'
            file = open(filename, 'rb')
            reader = csv.DictReader(file)
            matchedRows = []
            for row in reader:
                if (row[field] == value):
                    matchedRows.append(row)
            return matchedRows
        else:
            return meta().get()

api.add_resource(meta, '/')
api.add_resource(endpoint, '/<string:endpoint>')
api.add_resource(getRow, '/<string:endpoint>/<string:field>=<string:value>')

if __name__ == '__main__':
     app.run(port = int(os.environ.get('PORT', 33507)))

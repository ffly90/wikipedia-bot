import searcher
import yaml
import os
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

class Definition(Resource):
    def __init__(self, **kwargs):
        self.__indexList = kwargs['indexList']
        self.__config = kwargs['config']
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("searchVal")
        args = parser.parse_args()
        searchResult, multipleResults = searcher.binaryIndexSearch(self.__indexList, args['searchVal'])
        if not multipleResults and searchResult:
            return searcher.getText(self.__config, searchResult[1], searchResult[2]), 200
        elif multipleResults:
            return "\n".join(["Wähle eines der folgenden Ergebnisse aus:"] + searchResult), 200
        elif not multipleResults and not searchResult:
            return "Zum übergebenen Suchbegriff wurde keine Definition gefunden. Bitte versuchen Sie es mit einem anderen Begriff erneut.", 404

def main():
    app = Flask(__name__)
    api = Api(app)

    with open("config.yml","r") as configYaml:
        # opens config file and stores the information to a variable
        config = yaml.load(configYaml, Loader=yaml.SafeLoader)
    indexList = []
    with open(os.path.join(config['PATH_WIKI_XML'], config['FILENAME_SORTED_INDEX']), 'r') as index:
        print("Lade index...")
        for line in index.readlines():
            indexList.append(line.rstrip('\n').split('|'))
    api.add_resource(Definition, "/definition/", resource_class_kwargs={'indexList': indexList, 'config': config})
    app.run(debug=True)
    return

if __name__ == "__main__":
   exit(main())




from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import os, sys


app = Flask(__name__)
api = Api(app)

class fileListApi(Resource):
    def __init__(self): 
        global fileS 
        self.server = fileS  # Init the global server
        super(fileListApi, self).__init__()  
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('filename', type=str, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('data', type=str, location='json')
        self.reqparser.add_argument('version', type=int, location='json')

    def get(self):
        return self.server.files
        # return {"Hello": "World"} 
        
    def post(self):
        args = self.reqparser.parse_args()  
        f = {}
        for k, v in args.items():
            f[k] = v
        if any(d['filename'] == f['filename'] for d in self.server.files):
            return {'success':False}  
        else:
            self.server.files.append(f) 
            # Write to disk
            dir = os.path.dirname(__file__)  
            serverDataPath = os.path.join(dir, 'serverData1')  
            serverDataPath = os.path.join(serverDataPath, f['filename'])
            print(serverDataPath)
            currentFile = open(serverDataPath, 'w')
            currentFile.write(f['data'])
            currentFile.close()
            return {'success':True}

api.add_resource(fileListApi, "/filedir", endpoint="filelist")


if __name__ == "__main__":
    fileS = fileServer()  
    app.run(port=int(sys.argv[1]))

from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import os, sys


app = Flask(__name__)
api = Api(app)


class fileApi(Resource):
    def __init__(self):
        global fileS
        self.server = fileS
        super(fileApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()  # Init a request parser
        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('filename', type=str, location='json')  # Repeat for multiple variables
        self.reqparser.add_argument('version', type=int, location='json')
        self.reqparser.add_argument('data', type=str, location='json')
        # self.reqparser.add_argument('Client_ID', type=str, location = 'json')  # Repeat for multiple variables

    def get(self, filename):
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': False}  # Not in the list
        f = f[0]  # Take first element of f (should only be one)
        return f # f['filename'] to just get the name of the file
        

    def delete(self, filename):
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': False}  
        self.server.files[:] = [d for d in self.server.files if d.get('filename') != filename]

        dir = os.path.dirname(__file__)  
        serverDataPath = os.path.join(dir, 'serverData2')  
        serverDataPath = os.path.join(serverDataPath, filename)
        print(serverDataPath)

        if os.path.exists(serverDataPath):
            os.remove(serverDataPath)  
        print(self.server.files)
        return {'success':True}

    def put(self, filename):
        args = self.reqparser.parse_args()  
        print(args)
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': 'notOnServer'}
        f = f[0]  
        if args['version'] < f['version']:
            return {'success':'outOfDate'}

        args['version'] = args['version'] + 1  

        for k, v in args.items():
             if v != None:
                print(v)
                f[k] = v

        dir = os.path.dirname(__file__)  
        serverDataPath = os.path.join(dir, 'serverData2')
        serverDataPath = os.path.join(serverDataPath, f['filename'])
        print(serverDataPath)
        # Update file data on disk
        currentFile = open(serverDataPath, 'w')
        currentFile.write(f['data'])
        currentFile.close()
        print(f)
        return {'success':f}


api.add_resource(fileApi, "/filedir/<string:filename>", endpoint="file")

class fileListApi(Resource):
    def __init__(self): 
        global fileS  
        self.server = fileS  
        super(fileListApi, self).__init__()  
        self.reqparser = reqparse.RequestParser()


        self.reqparser.add_argument('filename', type=str, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('data', type=str, location='json')
        self.reqparser.add_argument('version', type=int, location='json')

    def get(self):
        return self.server.files
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
            serverDataPath = os.path.join(dir, 'serverData2')  
            serverDataPath = os.path.join(serverDataPath, f['filename'])
            print(serverDataPath)
            currentFile = open(serverDataPath, 'w')
            currentFile.write(f['data'])
            currentFile.close()
            return {'success':True}


api.add_resource(fileListApi, "/filedir", endpoint="filelist")

class fileServer():
    def __init__(self):

        self.files = []  

        dir = os.path.dirname(__file__)  
        filePath = os.path.join(dir, 'serverData2')  
        print("\nServer files found:\n")
        for fileName in os.listdir(filePath):
            if fileName.endswith(".txt"):  
                print(fileName)
                with open(os.path.join("serverData2", fileName), "r") as myfile:
                    data = myfile.readlines()
                self.files.append({'filename': fileName, "data": data, "version": 0})
        print("\n")


if __name__ == "__main__":
    fileS = fileServer()  
    app.run(port=int(sys.argv[1]))

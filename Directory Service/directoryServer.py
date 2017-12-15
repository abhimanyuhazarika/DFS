from flask import Flask
from flask_restful import Resource, Api , reqparse
import requests, json, sys

app = Flask(__name__)
api = Api(app)

class getFileLocation(Resource):
    def __init__(self): 
        global fileS  
        self.server = fileS  
        super(getFileLocation, self).__init__() 
        self.reqparser = reqparse.RequestParser()

        self.reqparser.add_argument('filename', type=str, location = 'json') 
        self.reqparser.add_argument('data', type=str, location='json')
        self.reqparser.add_argument('version', type=int, location='json')

    def get(self, filename):

        self.server.serverInfo['fileServer1']['serverFiles'] = []  
        self.server.serverInfo['fileServer2']['serverFiles'] = []  

        location = 'http://{}:{}/filedir'.format(self.server.serverInfo['fileServer1']['ip'],
                                                 self.server.serverInfo['fileServer1']['port'])
        r = requests.get(location)
        json_data = json.loads(r.text) 
        print("FileServer 1 files: {}".format(json_data))

        for x in json_data:
            self.server.serverInfo['fileServer1']['serverFiles'].append(x['filename'])

        location = 'http://{}:{}/filedir'.format('localhost', 5002)
        r = requests.get(location)
        json_data = json.loads(r.text) 
        print("FileServer 2 files: {}".format(json_data))

        for x in json_data:
            self.server.serverInfo['fileServer2']['serverFiles'].append(x['filename'])

        # Now that the file lists are up to date, can locate what server the file is on
        for x in self.server.serverInfo['fileServer1']['serverFiles']:
            if x == filename:
                return {'ip':self.server.serverInfo['fileServer1']['ip'],
                        'port':self.server.serverInfo['fileServer1']['port'],
                        'filename':filename}

        for x in self.server.serverInfo['fileServer2']['serverFiles']:
            if x == filename:
                return {'ip':self.server.serverInfo['fileServer2']['ip'],
                        'port':self.server.serverInfo['fileServer2']['port'],
                        'filename':filename}

        print(self.server.serverInfo)
        return {'ip':-1}

api.add_resource(getFileLocation, "/filedir/<string:filename>", endpoint="file")


class getFileList(Resource):
    def __init__(self):  
        global fileS  
        self.server = fileS  
        super(getFileList, self).__init__()  
        self.reqparser = reqparse.RequestParser()


        self.reqparser.add_argument('filename', type=str, location = 'json') 
        self.reqparser.add_argument('data', type=str, location='json')
        self.reqparser.add_argument('version', type=int, location='json')

    def get(self):
        return self.server.serverInfo

api.add_resource(getFileList, "/filedir", endpoint="filelist")


class getAServer(Resource):
    def __init__(self): 
        global fileS  
        self.server = fileS  
        super(getAServer, self).__init__()  
        self.reqparser = reqparse.RequestParser()

    def get(self):
        if self.server.serverCount == 1:
            self.server.serverCount = 2
            return self.server.serverInfo['fileServer1']
        elif self.server.serverCount == 2:
            self.server.serverCount = 1
            return self.server.serverInfo['fileServer2']

api.add_resource(getAServer, "/getServer", endpoint="getServer")

class fileServer():
    def __init__(self):
        self.serverCount = 1

        self.serverInfo = {'fileServer1':{'ip':sys.argv[1], 'port':int(sys.argv[2]), 'serverFiles':[]},
                           'fileServer2': {'ip':sys.argv[3], 'port': int(sys.argv[4]), 'serverFiles':[]}}
        location = 'http://{}:{}/filedir'.format(self.serverInfo['fileServer1']['ip'], self.serverInfo['fileServer1']['port'])
        r = requests.get(location)
        json_data = json.loads(r.text)
        print("FileServer 1 files: {}".format(json_data))

        for x in json_data:
            self.serverInfo['fileServer1']['serverFiles'].append(x['filename'])

        location = 'http://{}:{}/filedir'.format('localhost', 5002)
        r = requests.get(location)
        json_data = json.loads(r.text)  # JSON to dict
        print("FileServer 2 files: {}".format(json_data))

        for x in json_data:
            self.serverInfo['fileServer2']['serverFiles'].append(x['filename'])

if __name__ == "__main__":
    fileS = fileServer() 
    app.run(port=int(sys.argv[5]))

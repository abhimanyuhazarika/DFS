from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import os, sys

app = Flask(__name__)
api = Api(app)

class lockingFileAccess(Resource):
    def __init__(self):  
        global fileS  
        self.server = fileS 
        super(lockingFileAccess, self).__init__()  
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('id', type=int, location='json') 

    def put(self, filename):
        args = self.reqparser.parse_args() 
        if filename in self.server.locks:
            if args['id'] not in self.server.locks[filename]:
                self.server.locks[filename].append(args['id'])
                print("appended client {} to lock list for {}".format(args['id'], filename))
                print(self.server.locks)
                return {'success': 'Acquired'}
            else:
                print("already got that one")
                return {'success': 'Already in list'}  
        else:
            print("File not on server")
            return {'success': 'Not on server'}
        
    def delete(self, filename):
        args = self.reqparser.parse_args()
        if filename not in self.server.locks: 
            return {'success': 'Not on list'}
        if args['id'] in self.server.locks[filename]:
            self.server.locks[filename].remove(args['id'])
            print("Lock queue: {}".format(self.server.locks))
            return {'success':'Removed'}

        print("Not on list for some reason")
        return {'success': 'Not on list'}

api.add_resource(lockingFileAccess, "/lock/<string:filename>", endpoint="lock")


class lockingAcquire(Resource):
    def __init__(self):  
        global fileS  
        self.server = fileS  
        super(lockingAcquire, self).__init__()  

    def get(self):
        self.server.currentID += 1
        return {'id':self.server.currentID}


api.add_resource(lockingAcquire, "/lock", endpoint="lockID")

class fileListApi(Resource):
    def __init__(self):  
        global fileS 
        self.server = fileS 
        super(fileListApi, self).__init__()  
        self.reqparser = reqparse.RequestParser()

        self.reqparser.add_argument('filename', type=str, location = 'json')  
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
            return {'success':False}  # Already in the filesystem
        else:
            print(f)
            self.server.files.append(f)  
            self.server.locks[f['filename']] = []  
            print("Created lock buffer for {}\nCurrent Lock list: {}".format(f['filename'], self.server.locks))
            # Write to disk
            dir = os.path.dirname(__file__)  
            serverDataPath = os.path.join(dir, 'serverData')  
            serverDataPath = os.path.join(serverDataPath, f['filename'])
            print(serverDataPath)
            currentFile = open(serverDataPath, 'w')
            currentFile.write(f['data'])
            currentFile.close()
            return {'success':True}

api.add_resource(fileListApi, "/filedir", endpoint="filelist")


class fileApi(Resource):
    def __init__(self):
        global fileS
        self.server = fileS
        super(fileApi, self).__init__()  
        self.reqparser = reqparse.RequestParser()  
        self.reqparser.add_argument('filename', type=str, location='json')  
        self.reqparser.add_argument('version', type=int, location='json')
        self.reqparser.add_argument('data', type=str, location='json')
        self.reqparser.add_argument('clientID', type=int, location='json')

    def get(self, filename):
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': False}  # Not in the list
        f = f[0] 
        return f 


    def delete(self, filename):
        args = self.reqparser.parse_args() 
        print(args)
        if filename not in self.server.locks:
            return {'success': 'Not in list'}

        if args['clientID'] != self.server.locks[filename][0]:
            return {'success': 'locked'}

        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': False}  # Not in the list
        self.server.files[:] = [d for d in self.server.files if d.get('filename') != filename]
        self.server.locks.pop(filename, 0)
        print("Deleted lock buffer for {}\nCurrent Lock list: {}".format(filename, self.server.locks))

        dir = os.path.dirname(__file__)  
        serverDataPath = os.path.join(dir, 'serverData') 
        serverDataPath = os.path.join(serverDataPath, filename)
        print(serverDataPath)

        if os.path.exists(serverDataPath):
            os.remove(serverDataPath) 
        print(self.server.files)
        return {'success':True}

    def put(self, filename):
        args = self.reqparser.parse_args()  
        print(args)

        if args['clientID'] != self.server.locks[filename][0]:
            return {'success': 'locked'}
        # print(args['version'])
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
        serverDataPath = os.path.join(dir, 'serverData')  
        serverDataPath = os.path.join(serverDataPath, f['filename'])
        print(serverDataPath)
        currentFile = open(serverDataPath, 'w')
        currentFile.write(f['data'])
        currentFile.close()
        print(f)
        return {'success':f}
    
api.add_resource(fileApi, "/filedir/<string:filename>", endpoint="file")


class fileServer():
    def __init__(self):

        self.files = [] 
        self.locks = {}  

        dir = os.path.dirname(__file__)  
        filePath = os.path.join(dir, 'serverData')  
        print("\nServer files found:\n")
        for fileName in os.listdir(filePath):
            if fileName.endswith(".txt"): 
                print(fileName)
                with open(os.path.join("serverData", fileName), "r") as myfile:
                    data = myfile.readlines()
                self.files.append({'filename':fileName, "data":data, "version":0})
                self.locks[fileName] = []
        print("\n")
        self.currentID = 0


if __name__ == "__main__":
    fileS = fileServer() 
    app.run(port=int(sys.argv[1]))

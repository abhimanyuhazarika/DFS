from flask import Flask
from flask_restful import Resource, Api, reqparse
import os, sys


app = Flask(__name__)
api = Api(app)

class fileServer():
    def __init__(self):
        self.files = []  

        dir = os.path.dirname(__file__)  
        filePath = os.path.join(dir, 'serverData')  
        print("\nServer files found:\n")
        for fileName in os.listdir(filePath):
            if fileName.endswith(".txt"):
                print(fileName)
                with open(os.path.join("serverData", fileName), "r") as myfile:
                    data = myfile.readlines()
                self.files.append({'filename': fileName, "data": data, "version": 0})
        print("\n")
        print(f)
        return {'success':f}



if __name__ == "__main__":
    fileS = fileServer() 

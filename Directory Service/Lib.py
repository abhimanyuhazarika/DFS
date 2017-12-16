import requests, json


def listFiles(ip, port):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.get(location)
    direct_data = json.loads(r.text)  

    for key in direct_data:
        print("Files from {}".format(key))
        location = 'http://{}:{}/filedir'.format(direct_data[key]['ip'], direct_data[key]['port'])
        r = requests.get(location)
        json_data = json.loads(r.text) 
        print("List of files on file server:\n")
        for x in json_data:
            print("--------------------------")
            print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(x['filename'], x['version'], ''.join(x['data'])))
            print("--------------------------")


def getFile(ip, port, filename):
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.get(location)
    direct_data = json.loads(r.text) 
    if direct_data['ip'] == -1:
        print("(getFile) File does not exist on server")
        return -1

    # File Server access
    location = 'http://{}:{}/filedir/{}'.format(direct_data['ip'], direct_data['port'], direct_data['filename'])
    r = requests.get(location)
    json_data = json.loads(r.text)  
    if 'success' in json_data:
        if json_data['success'] == False:
            print("(getFile) File does not exist on server")
            return -1
    return json_data

def editFile(ip, port, fileDict, newText):
    # Directory service access
    location = 'http://{}:{}/filedir/{}'.format(ip, port, fileDict['filename'])
    r = requests.get(location)
    direct_data = json.loads(r.text)  # JSON to dict (JSON)
    if direct_data['ip'] == -1:
        print("(editFile) File does not exist on server")
        return -1

    # Edit the file
    fileDict['data'] = newText
    location = 'http://{}:{}/filedir/{}'.format(direct_data['ip'], direct_data['port'], direct_data['filename'])
    r = requests.put(location, json={'version': fileDict['version'], 'data':fileDict['data']})
    json_data = json.loads(r.text)
    if json_data['success'] == 'notOnServer':
        print("(editFile) File does not exist on server")
    elif json_data['success'] == 'outOfDate':
        print("(editFile) File is behind on version")
        return -1


def createFile(ip, port, filename, data):
    # Get info for a single file server
    location = 'http://{}:{}/getServer'.format(ip, port)  
    r = requests.get(location)
    direct_data = json.loads(r.text)  # convert from JSON to text

    # Create the file
    location = 'http://{}:{}/filedir'.format(direct_data['ip'], direct_data['port'])
    r = requests.post(location, json={'filename': filename, 'version': 0, 'data': data})
    json_data = json.loads(r.text)
    if json_data['success'] == False:
        print("(createFile) The file already exists")
    else:
        print("Created file on server at {}:{}".format(direct_data['ip'], direct_data['port']))

def deleteFile(ip, port, filename):
    # Directory service access
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.get(location)
    direct_data = json.loads(r.text)  # JSON to dict (JSON)
    if direct_data['ip'] == -1:
        print("(getFile) File does not exist on server")
        return -1

    location = 'http://{}:{}/filedir/{}'.format(direct_data['ip'], direct_data['port'], direct_data['filename'])
    r = requests.delete(location)
    json_data = json.loads(r.text)  
    if 'success' in json_data:
        if json_data['success'] == False:
            print("(deleteFile) File does not exist on server")
            return -1
        elif json_data['success'] == True:
            print("Successful deletion")

def printFile(fileDict):

    print("--------------------------")
    print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(fileDict['filename'], fileDict['version'], ''.join(fileDict['data'])))
    print("--------------------------")

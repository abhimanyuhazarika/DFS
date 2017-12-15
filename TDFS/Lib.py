import requests, json

def listFiles(ip, port, clientCache):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.get(location)
    json_data = json.loads(r.text)  
    print("Server File List:\n")
    for x in json_data:
        print("--------------------------")
        print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(x['filename'], x['version'], ''.join(x['data'])))
        print("--------------------------")

    print("Cache file List:\n")
    for x in clientCache:
        print("--------------------------")
        print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(x['filename'], x['version'], ''.join(x['data'])))
        print("--------------------------")

def getFile(ip, port, filename, clientCache):
    f = [f for f in clientCache if f['filename'] == filename]  

    if len(f) == 0: 
        print("(getFile) Not in cache")
        location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
        r = requests.get(location)
        json_data = json.loads(r.text)  
        if 'success' in json_data:
            if json_data['success'] == False:
                print("(getFile) File does not exist on server")
                return -1
        # Storing it in the local cache
        clientCache.append(json_data)

    else:  
        print("(getFile) Found in cache")
        f = f[0]  
        print(f)
        return f

    print(json_data)
    return json_data


def editFile(ipAddress, portNumber, clientID, fileData, newText, clientCache):
    #  changing only the cached version
    f = [f for f in clientCache if f['filename'] == fileData['filename']]  # check if in cache
    f = f[0]
    if len(f) == 0:  # not in cache yet
        print("(Edit file) File not in cache")
    f['data'] = newText  # Edited cached version
    print(clientCache)


def uploadFile(ip, port, clientID, filename, clientCache):
    # uploading file from the cache
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    f = [f for f in clientCache if f['filename'] == filename]  # check if in cache
    if len(f) == 0:  
        print("(Upload file) File not in cache")
        return
    f = f[0]
    print(filename, "printing File Name:")
    r = requests.put(location, json={'version': f['version'], 'data':f['data'], 'clientID':clientID})
    json_data = json.loads(r.text)
    if json_data['success'] == 'locked':
        print("(editFile) This file is currently locked. Waiting")
        return -1
    elif json_data['success'] == 'notOnServer':
        print("(uploadFile) File does not exist on server")
    elif json_data['success'] == 'outOfDate':
        print("(uploadFile) File is behind on version. Get the updated version")
        clientCache.remove(f)
        print("{} removed from cache".format(f['filename']))
        return -1

def createFile(ip, port, filename, data, clientCache):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.post(location, json={'filename': filename, 'version': 0, 'data': data})
    json_data = json.loads(r.text)
    if json_data['success'] == False:
        print("(createFile) The file already exists")
        return
    clientCache.append({'filename': filename, 'version': 0, 'data': data})


def deleteFile(ip, port,clientID, filename, clientCache):
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.delete(location, json={'clientID':clientID})
    json_data = json.loads(r.text)  
    if 'success' in json_data:
        if json_data['success'] == 'locked':
            print("(deleteFile) File is locked. Waiting...")
            return -1
        elif json_data['success'] == False:
            print("(deleteFile) File does not exist on server")
            return -1
        elif json_data['success'] == True:
            print("Successful deletion")
    f = [f for f in clientCache if f['filename'] == filename]
    if len(f) == 0:
        return
    f = f[0]
    clientCache.remove(f)
    print("Removed {} from cache".format(f['filename']))

def printFile(fileDict):

    print("--------------------------")
    print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(fileDict['filename'], fileDict['version'], ''.join(fileDict['data'])))
    print("--------------------------")
def lockGetId(ip, port):
    location = 'http://{}:{}/lock'.format(ip, port)
    r = requests.get(location)
    json_data = json.loads(r.text)
    clientID = json_data['id']
    return clientID

def lockAddToQueue(ip, port, clientID, filename):
    r = requests.put('http://{}:{}/lock/{}'.format(ip, port, filename), json={'id': clientID})
    json_data = json.loads(r.text)  
    if json_data['success'] == 'Acquired':
        print("Added to lock queue for {}".format(filename))
    else:
        print("Not added to lock queue")

def lockDeleteFromQueue(ip, port, clientID, filename):
    r = requests.delete('http://{}:{}/lock/{}'.format(ip, port, filename), json={'id': clientID})
    json_data = json.loads(r.text)  
    if json_data['success'] == 'Removed':
        print("Removed from lock queue for {}".format(filename))

import Lib, time, sys

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
# r = requests.get()
# r_text = r.json()

def run():
    # ipAddress = input("Enter the IP of the fileserver: ")
    # portNumber = input("Enter the port number of the fileserver: ")
    localCache = []
    ipAddress = sys.argv[1]
    portNumber = int(sys.argv[2])
    print("IP:{} Port:{}".format(ipAddress,portNumber))

    # Acquire Client ID
    clientID = Lib.lockGetId('localhost', 8001)

    running = True
    while running:
        userChoice = input("Enter the number for the specified action\n"
                           "1) List all files in server and cache\n"
                           "2) Read file\n"
                           "3) Create new file\n"
                           "4) Write to file\n"
                           "5) Delete a file\n"
                           "6) Push file to server\n"
                           "0) Exit client application\n")
        if userChoice == '1':
            Lib.listFiles(ipAddress, portNumber, localCache)

        elif userChoice == '2':
            userFile = input("Enter the file name: ")  # must include file extension
            fileRecv = Lib.getFile(ipAddress, portNumber, userFile, localCache)
            if fileRecv != -1:
                Lib.printFile(fileRecv)

        elif userChoice == '3':
            userFile = input("Enter new file name: ")
            userData = input("Enter data for the file: ")
            Lib.createFile(ipAddress, portNumber, userFile, userData, localCache)
            
        elif userChoice == '4':
            userFile = input("Enter file name: ")
            #Lib.editFile(ipAddress, portNumber, clientID, fileRecv, dataToWrite, localCache)
            fileRecv = Lib.getFile(ipAddress, portNumber, userFile, localCache)
            if fileRecv != -1:
                Lib.printFile(fileRecv)
                #Lib.lockAddToQueue(ipAddress, portNumber, clientID, userFile)  # Join lock queue

                lockStatus = -1
                while lockStatus == -1:  # Polling
                    dataToWrite = input("Enter the data to write to the file: ")
                    lockStatus = Lib.editFile(ipAddress, portNumber, clientID, fileRecv, dataToWrite, localCache)
                    if lockStatus != -1:
                        break
                    if input("Type '0' to abort edit. Type anything else to wait:") == '0':
                        break
                    time.sleep(2)
                #Lib.lockDeleteFromQueue(ipAddress, portNumber, clientID, userFile)  # Leave lock queue
            else:
                print("File not found\n")  

        elif userChoice == '5':
            userFile = input("Enter the file name to delete: ")
            Lib.lockAddToQueue(ipAddress, portNumber, clientID, userFile)  # Join lock queueue
            lockStatus = -1
            while lockStatus == -1:  # Polling
                lockStatus = Lib.deleteFile(ipAddress, portNumber, clientID, userFile, localCache)
                if lockStatus != -1:
                    break
                if input("Type '0' to abort deletion. Type anything else to wait:") == '0':
                    break
                time.sleep(2)
            Lib.lockDeleteFromQueue(ipAddress, portNumber, clientID, userFile)  # Leave lock queue

        elif userChoice == '6':
            userFile = input("Enter the filename to push to the server: ")
            #Lib.uploadFile(ipAddress, portNumber, userFile, localCache)
            fileRecv = Lib.getFile(ipAddress, portNumber, userFile, localCache)
            if fileRecv != -1:
                Lib.printFile(fileRecv)
                Lib.lockAddToQueue(ipAddress, portNumber, clientID, userFile)  # Join lock queue

                lockStatus = -1
                while lockStatus == -1:  # Polling
                    dataToWrite = input("Enter the data to write to the file:")
                    lockStatus = Lib.uploadFile(ipAddress, portNumber, clientID, userFile, localCache)
                    if lockStatus != -1:
                        break
                    if input("Type '0' to abort edit. Type anything else to wait:") == '0':
                        break
                    time.sleep(2)
                Lib.lockDeleteFromQueue(ipAddress, portNumber, clientID, userFile)  # Leave lock queue
            else:
                print("File not found\n")

        elif userChoice == '0':
            print("Ending client application")
            running = False


if __name__ == "__main__":
    run()

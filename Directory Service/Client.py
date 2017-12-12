import clientLibrary, sys

def run():
    ipAddr = sys.argv[1]
    portNumber = int(sys.argv[2])
    print("IP:{} Port:{}".format(ipAddr,portNumber))
    running = True
    while running:
        userChoice = input("Enter an option\n"
                           "1. List all files\n"
                           "2. Read file\n"
                           "3. Write to an existing file\n"
                           "4. Create new file\n"
                           "5. Delete file\n"
                           "0. Exit\n")
        if userChoice == '1':
            clientLibrary.listFiles(ipAddr,portNumber)

        elif userChoice == '2':
            userFile = input("Enter the file name: ")
            fileRecv = clientLibrary.getFile(ipAddr, portNumber, userFile)
            if fileRecv != -1:
                clientLibrary.printFile(fileRecv)

        elif userChoice == '3':
            userFile = input("Enter the file name: ")
            fileRecv = clientLibrary.getFile(ipAddr, portNumber, userFile)
            if fileRecv != -1:
                clientLibrary.printFile(fileRecv)
                clientLibrary.lockAddToQueue(ipAddr, portNumber, clientID, userFile)

                lockStatus = -1
                while lockStatus == -1: 
                    dataToWrite = input("Type the text you want to write to the file: ")
                    lockStatus = clientLibrary.editFile(ipAddr, portNumber, clientID, fileRecv, dataToWrite)
                    if lockStatus != -1:
                        break
                    if input("Type '0' to abort edit. Type anything else to wait:") == '0':
                        break
                    time.sleep(2)
                clientLibrary.lockDeleteFromQueue(ipAddr, portNumber, clientID, userFile)
            else:
                print("File not found\n")

        elif userChoice == '4':
            userFile = input("Enter new file name: ")
            userData = input("Enter new data for the file: ")
            clientLibrary.createFile(ipAddr, portNumber, userFile, userData)

        elif userChoice == '5':
            userFile = input("Enter the file name to delete: ")
            clientLibrary.lockAddToQueue(ipAddr, portNumber, clientID, userFile)
            lockStatus = -1
            while lockStatus == -1:
                lockStatus = clientLibrary.deleteFile(ipAddr, portNumber, clientID, userFile)
                if lockStatus != -1:
                    break
                if input("Type '0' to abort deletion. Type anything else to wait:") == '0':
                    break
                time.sleep(2)
            clientLibrary.lockDeleteFromQueue(ipAddr, portNumber, clientID, userFile) 

        elif userChoice == '0':
            print("Ending client application")
            running = False


if __name__ == "__main__":
    run()

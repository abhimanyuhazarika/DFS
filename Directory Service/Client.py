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
                dataToWrite = input("Type the text you want to write to the file: ")
                clientLibrary.editFile(ipAddr, portNumber, fileRecv, dataToWrite)
            else:
                print("File not found\n")

        elif userChoice == '4':
            userFile = input("Enter new file name: ")
            userData = input("Enter new data for the file: ")
            clientLibrary.createFile(ipAddr, portNumber, userFile, userData)

        elif userChoice == '5':
            userFile = input("Enter the file name to delete: ")
            clientLibrary.deleteFile(ipAddr, portNumber, userFile)

        elif userChoice == '0':
            print("Ending client application")
            running = False


if __name__ == "__main__":
    run()

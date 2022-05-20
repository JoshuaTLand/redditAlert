from os import path

def saveToken(token):
    with open('token', 'w+') as f:
        f.truncate()
        f.write(token)

def readToken():
    if not path.isfile('token'):
        with open('token', "w+") as file:
            file.write("token")
    with open('token', 'r') as f:
        return f.readline()

def loadSubList(fileName):
    if not path.isfile(fileName):
        with open(fileName, "w+") as file:
            file.write("all")

    subList = []

    with open(fileName, "r") as file:
        fileList = file.readlines()
        for item in fileList:
            if not item.startswith('#') and item.strip():
                subList.append(item)

    return subList





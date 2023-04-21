from pymongo import MongoClient
from exceptions import AlreadyExistsError
import certifi

ca = certifi.where()
dbURL = "mongodb+srv://anshulkumar:zziETGmWqHK1l0HI@cluster0.fupwqgv.mongodb.net/?retryWrites=true&w=majority"

def addNewUser(username, password):
    with MongoClient(dbURL, tlsCAFile = ca) as org:
        usersDB = org["Users"]
        usersCols = usersDB.list_collection_names()
        if username in usersCols:
            return False
        else:
            newUser = usersDB[username]
            insert = {"Username":username, "Password":password}
            newUser.insert_one(insert)
            return True

def authenticateUser(username, password):
    with MongoClient(dbURL, tlsCAFile = ca) as org:
        usersDB = org["Users"]
        usersCols = usersDB.list_collection_names()

        if username not in usersCols:
            return False
        
        myUser = usersDB[username]
        myPassword = myUser.find_one()["Password"]

        if myPassword != password:
            return False
        
        return True
    
def addNewProject(user, projectID, projectName, desc):
    with MongoClient(dbURL, tlsCAFile = ca) as org:
        projectsDB = org["Projects"]
        projectsCols = projectsDB.list_collection_names()
        if projectID in projectsCols:
            return False
        else:
            newProject = projectsDB[projectID]
            insert = {"ProjectID":projectID, "ProjectName":projectName, "Users":[user], "Desc":desc,
                      "Checkedout": 0}
            newProject.insert_one(insert)
            return True
        
def authenticateProject(user, projectID):
    with MongoClient(dbURL, tlsCAFile = ca) as org:
        projectsDB = org["Projects"]
        projectsCols = projectsDB.list_collection_names()
        if projectID not in projectsCols:
            return False
        project = projectsDB[projectID].find_one()
        # if user not in project["Users"]:
        #     return False
        return True
    
def getProjectInfo(projectID):
    with MongoClient(dbURL, tlsCAFile = ca) as org:
        projectsDB = org["Projects"]
        projectsCols = projectsDB.list_collection_names()
        if projectID not in projectsCols:
            return None
        project = projectsDB[projectID].find_one()
        return project["ProjectName"], project["Users"], project["Desc"]

def addUserToProject(user, projectID):
    with MongoClient(dbURL, tlsCAFile = ca) as org:
        projectsDB = org["Projects"]
        projectsCols = projectsDB.list_collection_names()
        if projectID not in projectsCols:
            return False
        doc = projectsDB[projectID].find_one()
        doc["Users"] = doc["Users"].append(user)
        query = {"ProjectID":projectID}
        projectsDB[projectID].update_one(query, {"$set": {"Users":doc["Users"]}})
        return True
    
def checkoutHardware(name, amount, projectID):
    with MongoClient(dbURL, tlsCAFile = ca) as org:
        hardwareDB = org["Hardware"]
        projectDB = org["Projects"]
        hardwareCols = hardwareDB.list_collection_names()
        if name not in hardwareCols:
            return False
        projectCols = projectDB.list_collection_names()
        if projectID not in projectCols:
            return False
        doc = hardwareDB[name].find_one()
        projDoc = projectDB[projectID].find_one()
        if doc["Amount"] < amount:
            return False
        if amount < 0 and (projDoc["Checkedout"] + amount < 0):
            return False
        query = {"_id":doc["_id"]}
        hardwareDB[name].update_one(query, {"$set": {"Amount":doc["Amount"] - amount}})
        query = {"ProjectID":projectID}
        projectDB[projectID].update_one(query, {"$set": {"Checkedout":projDoc["Checkedout"] + amount}})
        return True

def getHardware(name):
    with MongoClient(dbURL, tlsCAFile = ca) as org:
        hardwareDB = org["Hardware"]
        doc = hardwareDB[name].find_one()
        return doc["Amount"], doc["Capacity"]

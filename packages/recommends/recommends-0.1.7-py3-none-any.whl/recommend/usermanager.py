from recommend.user import User
import json
from recommend.location import Location
from recommend.history import History
import os

class UserManager:
    def __init__(self, storedRecordOfUsers:str = None):
        if storedRecordOfUsers is None:
            self.users = []
            self.UserIds = []

        else:
            self.loadUsersFromFile(storedRecordOfUsers)
            

    def loadUsersFromFile(self, locationOfUserData:str):
        try:
            with open(locationOfUserData, "r") as file:
                data = json.loads(file.read())
                
                for user in data.values():
                    if user["id"] in self.UserIds:
                        continue
                    else:
                        self.users.append(User(id= user["id"], history=History().setHistory(user["history"]), location=Location().setLocation(user["location"][0], user["location"][1])))
                        self.UserIds.append(user["id"])


        except IOError as ioerr:
            print(f"There was an error with loading the file: {ioerr}")
            cwd = os.getcwd()  # Get the current working directory (cwd)
            files = os.listdir(cwd)  # Get all the files in that directory
            print("Files in the current directory are %s" % (files))

        except:
            print("Unexpected Error in initializing the users")

    def saveUsersToFile(self, saveLocation):
        data = []

        for user in self.users:
            data.append(user.objectToDict())

        with open(saveLocation, "w") as file:
            file.write(json.dumps(data, indent=4))

    def addUser(self, user:User):
        self.users.append(user)

    def searchForUser(self, id):
        for user in self.users:
            if(user.getId() == id):
                return user
        
        return f"User with id{id} doesn't exist"
    
    def removeUser(self, userId):
        for user in self.users:
            if user.id == userId:
                self.users.remove(user)
                return user
        
        return "User doesn't exist"
    
    def returnUsersWithHistoryHavingRecordWithId(self, id):
        values = []

        for user in self.users:
            for history in user.getHistory():
                if history[1] == id:
                    values.append(user)

    def returnUsersWithHistoryHavingRecordWithIdInCategory(self, id:str, category:str):
        values = []

        for user in self.users:
            for history in user.getHistory():
                if history[0] == category and history[1] == id:
                    values.append(user)
        
        return values
    
    def getUsersInRangeOfLocation(self, meters, location:Location):
        usersInRange = []

        for user in self.users:
            if(self.distanceToLocationInMeters(location, user.getLocation()) <= meters):
                usersInRange.append(user)
            
    def getUsersWithSimilarHistories(self, userToCompare:User, percentage = 50, maximum = 10, otherUsers = None):
        values = []
        lengthOfUserHistory = len(userToCompare.getHistory())

        if lengthOfUserHistory == 0:
            return "User has no history"

        container = None

        if otherUsers is None:
            container = self.users

        else:
            container = otherUsers

        for user in container:
            similarInterests = 0
            for history in user.getHistory():
                if history in userToCompare.getHistory():
                    similarInterests += 1
            
            similarity = (similarInterests / lengthOfUserHistory) * 100

            if similarity > percentage:
                values.append([user, similarInterests, similarity])

        if len(values) < maximum:
            return values
        
        else:
            return values[:maximum]

    def getSortedListOfUsersBasedOnSimilarity(self, users:list, maximum = 10):
        sortedList = []
        highest = 0
        indexesWithHighestNumbers = []
        iterations = maximum

        if len(users) < maximum:
            iterations = len(maximum)

        for a in range(iterations):
            UserWithHighest:User = None
            for i in range(len(users)):
                if users[i][1] > highest and i not in indexesWithHighestNumbers:
                    highest = users[i][1]
                    UserWithHighest = users[i]

            sortedList.append(UserWithHighest)

        return sortedList

    def getAllUsers(self):
        return self.users
    
    def distanceToLocationInMeters(self, locationOrigin:Location ,locationDestination:Location):
        disty = locationDestination.getLocationInFloat()[1] - locationOrigin.getLocationInFloat()[1]
        distx = locationDestination.getLocationInFloat()[0] - locationOrigin.getLocationInFloat()[0]

        sqry = disty**2
        sqrx = distx**2

        addition = sqry + sqrx

        distance = addition**0.5

        return distance * 111111
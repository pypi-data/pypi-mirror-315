#Users Class
from recommend.history import History
from recommend.location import Location
import json

class User:

    def __init__(self, id:str, history:History = None, location:Location = None):
        self.id = id

        if location is None:
            self.location = "Unknown"
        else:
            self.location = location

        if history is None:
            self.history:History = History()
        else:
            self.history:History = history.getHistory()

    def addToHistory(self, data:list):
        self.history.addToHistory(data)

    def deleteFromHistory(self, id:str, category:str=None):
        self.history.deleteRecordInHistory(id, category)

    def searchInHistory(self, id:str, category:str = None):
        return self.history.searchForRecordInHistory(id, category)

    def getLocation(self):
        return self.location
    
    def setLocation(self, location:Location):
        self.location = location
    
    def getId(self):
        return self.id

    def objectToDict(self):
        return {f"user{self.id}": {"id": self.id, "history": self.history.objectToDict(), "location": self.getLocation()}}
    
    def toJSON(self):
        return json.dumps(self.objectToDict(), indent=4)
    
    def getHistory(self):
        return self.history
    
    def setHistory(self, history:History):
        self.history = history

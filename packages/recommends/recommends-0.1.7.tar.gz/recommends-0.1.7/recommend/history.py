"""
A python file containing records such as movies, music, notifications and anyother categories
"""
import json

class History:

    def __init__(self):
        self.history = []

    def addToHistory(self, data:list):
        self.history.append(data)

    def deleteRecordInHistory(self, id:str, category:str = None):
        if category is None:
            for record in self.history:
                if record[1] == id:
                    self.history.remove(record)

        else:
            for record in self.history:
                if record[0] == category and record[1] == id:
                    self.history.remove(record)

    def searchForRecordInHistory(self, id:str, category:str = None):

        if category is None:
            for record in self.history:
                if record[1] == id:
                    return True

        else:
            for record in self.history:
                if record[1] == id and record[0] == category:
                    return True
                
        return False

    def getHistory(self):
        return self.history
    
    def setHistory(self, data:list):
        self.history = data
    
    def viewHistory(self):
        string = "History\n"

        for record in self.history:
            string += f"\t{record[0]} -> {record[1]}\n"

        return string
    
    def toJSON(self):
        categories = []
        data = {}

        for record in self.history:
            if record[0] not in categories:
                categories.append(record[0])

        for category in categories:
            data[category] = []
            for record in self.history:
                    data[category].append(record[1])

        
        return json.dumps(data)
    
    def objectToDict(self):
        return {"history": self.getHistory()}
# A storage engine for the data present within the system like movies, music and notifications
import json
import os

class StorageEngine:
    def __init__(self, storageFileLocation:str = None):
        self.data = {}

        if storageFileLocation is None:
            self.data = {}
        
        else:
            try:
                file = open(storageFileLocation, "r")
                self.data = json.loads(file.read())

            except IOError as ioerror:
                print(f"There was an error opening the file for reading. Error: {ioerror}")
                cwd = os.getcwd()  # Get the current working directory (cwd)
                files = os.listdir(cwd)  # Get all the files in that directory
                print("Files in the current directory are %s" % (files))

            except:
                print("There was an error initializing the Storage Engine")

    def getSavedData(self):
        return self.data
    
    def returnCategoriesOfStoredData(self):
        categories = []

        for key in self.data.keys():
            categories.append(key)

        return categories

    def returnDataInCategory(self, category):
        values = []

        if category not in self.data.keys():
            return "Category Doesn't Exist"

        for value in self.data[category]:
            values.append(value)

        return values
    
    def loadData(self, storageLocation):
        try:

            file = open(storageLocation, "r")
            loadedData = json.loads(file.read())

            for category in loadedData.keys():
                if category not in self.data.keys():
                    self.data[category] = loadedData[category]

                else:
                    for example in loadedData[category].keys():
                        self.data[category][self.data[category][example]]  = loadedData[category][example]


        except IOError as ioError:
            print(f"Error: {ioError}")

    def saveData(self, saveLocation):
        try:
            file = open(saveLocation, "w")
            
            saveddata = json.dumps(self.data, indent=4)

            file.write(saveddata)

            file.close()

        except IOError as ioErr:
            return ioErr
        
    def doesCategoryExist(self, category) -> bool:
        if category in self.data.keys():
            return True
        
        else:
            return False
        
    def doesRecordExist(self, id):
        for value in self.data.values():
            for subvalue in value.keys():
                if id == subvalue:
                    return True
                
        return False
    
    def getRecordWithId(self, id:str):
        for category in self.data.values():
            if id in category.keys():
                return category[id]
            
            else:
                return "Record Not Present"
    
    def getRecordWithIdAndCategory(self, id:str, category:str):
        if category not in self.data.keys():
            return "Record Doesn't Exist"
            
        else:
            if id not in self.data[category].keys():
                return f"Record with id{id} doesn't exist"
            
            else:
                for record in self.data.values():
                    if id in record.keys():
                        return record[id]
                        
                    else:
                        return "Record Not Present"
                            
    def getRecordsWithIdsInCategory(self, ids:list, category:str):
        values = []
        idsNotPresent = []

        if category not in self.data.keys():
            return f"Records Don't Exist"
            
        else:
            for id in ids:
                if id not in self.data[category].keys():
                    idsNotPresent.append(id)
                    continue
                    
                else:
                    if id in self.data[category].keys():
                        values.append(self.data[category][id])

            return (values, idsNotPresent)
        
    def getRecordsInCategory(self, category:str):
        if category not in self.data.keys():
            return "Category Doesn't exist"
        
        values = []
        for record in self.data[category].values():
            values.append(record)

        return values
    
    def getAllRecords(self):
        values = []
        for category in self.data.keys():
            for value in self.data[category].values():
                values.append(value)

        return values

    def getRecordsWithIdsInMultipleCategories(self, ids:list, categories:list):
        values = []
        idsNotPresent = []
        categoriesNotPresent = []

        for category in categories:
            if category not in self.data.keys():
                categoriesNotPresent.append(category)
                continue
            
            else:
                for id in ids:
                    if id not in self.data[category].keys():
                        idsNotPresent.append(id)
                        continue
                    
                    else:
                        for record in self.data[category].values():
                                if id in record.keys():
                                    values.append(record)
        return (values, idsNotPresent, categoriesNotPresent)
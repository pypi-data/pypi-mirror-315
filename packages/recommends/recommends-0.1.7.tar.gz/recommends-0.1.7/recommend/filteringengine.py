# a filtering engine for the recommendation library

class FilteringEngine: 

    def doesLabelExist(self, label, dataInQuestion:list):
        for data in dataInQuestion:
            if label not in data.keys():
                return False
            
            return True
        
    def getRecordsWithLabels(self, labels:list, data:list):

        values = []

        for dataValue in data:
            for label in labels:
                if label in dataValue.keys() and dataValue not in values:
                    values.append(dataValue)

        return values
                    
    def getRecordsWithLabel(self, label, data:list):
        values = []

        for value in data:
            if label in value.keys():
                values.append(value)

        return values
    
    def getLabels(self, data:dict):
        values = []

        for dataPoint in data:
            for label in dataPoint.keys():
                if label not in values:
                    values.append(label)

        return values

    def getValuesWithSubstring(self, data:dict, substring:str):
        values = []
        
        for dataPoint in data:
            for value in dataPoint.values():
                
                if isinstance(value, str) and value.find(substring) != -1:
                    values.append(dataPoint)

                if value is list:
                    for valueDetailed in value:
                        if valueDetailed.find(substring) != -1:
                            values.append(valueDetailed)

        return values
    
    def getRecordsWithValuesGreaterThan(self, data:dict, base, fieldName:str):

        values = []

        for dataPoint in data:

            if fieldName not in dataPoint.keys():
                continue

            else:
                for value in dataPoint:
                    if value[fieldName] > base:
                        values.append(dataPoint)

        return values
    
    def getRecordsWithValuesLessThan(self, data:dict, base, fieldName:str):

        values = []
        for dataPoint in data:

            if fieldName not in dataPoint.keys():
                continue

            else:
                for value in dataPoint:
                    if value[fieldName] < base:
                        values.append(dataPoint)

        return values
    
    def getRecordsWithValuesEqualTo(self, data:dict, base, fieldName:str):

        values = []
        for dataPoint in data:

            if fieldName not in dataPoint.keys():
                continue

            else:
                for value in dataPoint:
                    if value[fieldName] == base:
                        values.append(dataPoint)

        return values
    
    def getRecordsWithValuesLessThanOrEqualTo(self, data:dict, base:int, fieldName:str):

        values = []

        for dataPoint in data:

            if fieldName not in dataPoint.keys():
                continue

            else:
                for value in dataPoint:
                    if value[fieldName] <= base:
                        values.append(dataPoint)

        return values
    
    def getRecordsWithValuesGreaterThanOrEqualTo(self, data:dict, base:int, fieldName:str):

        values = []

        for dataPoint in data:

            if fieldName not in dataPoint.keys():
                continue

            else:
                for value in dataPoint:
                    if value[fieldName] >= base:
                        values.append(dataPoint)

        return values
    
    def sortRecords(self, data:list, labelToUse:str):

        dataSieved = []
        values = []
        highest = 0
        highestIndex = -1
        takenIndexes = []

        for dataPoint in data:
            if labelToUse in dataPoint.keys():
                dataSieved.append(dataPoint)

        for i in range(len(dataSieved)):
            highestIndex = 0
            highest = -1
            for a in range(len(dataSieved)):
                if dataSieved[a][labelToUse] > highest and a not in takenIndexes:
                    highest = dataSieved[a][labelToUse]
                    highestIndex = a
                
            takenIndexes.append(highestIndex)

            values.append(dataSieved[highestIndex])
    
        return values
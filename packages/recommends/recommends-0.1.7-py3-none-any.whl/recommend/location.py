# A class to keep track of location

class Location:
    def __init__(self, latitude:str, longitude:str, region:str = None):
        self.latitude = latitude
        self.longitude = longitude
        
        if region is None:
            self.region = "Unknown"
        else:
            self.region = region

    def getRegion(self):
        return self.region
    
    def getLongitude(self):
        return self.longitude
    
    def getLatitude(self):
        return self.latitude
    
    def setLatitude(self, latitude:str):
        self.latitude = latitude

    def setLongitude(self, longitude:str):
        self.longitude = longitude

    def setRegion(self, region:str):
        self.region = region

    def getLocationInFloat(self):
        return [float(self.latitude), float(self.longitude)]

    def getLocation(self):
        return [self.getLatitude(), self.getLongitude()]
    
    def setLocation(self, latitude:str, longitude:str):
        self.longitude = longitude
        self.latitude = latitude
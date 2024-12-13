# Recommendation Engine for the library
from recommend.storageengine import StorageEngine
from recommend.filteringengine import FilteringEngine
from recommend.usermanager import UserManager
from recommend.user import User
from recommend.location import Location

class RecommendationEngine:
    def __init__(self, id:str, storageEngineToQuery:StorageEngine, filter:FilteringEngine, userManager:UserManager ):
        if id is not None:
            self.id = id
        
        else:
            self.id = -1

        if storageEngineToQuery is not None:
            self.storageEngine = storageEngineToQuery

        if filter is not None:
            self.filter = filter

        if userManager is not None:
            self.userManager = userManager
        
    def recommendationsBasedOnSimilarity(self, userForComparison:User, maximumRecommendations = 10):

        if user is not User:
            return f"User isn't registered in the list of users. Perhaps you should recommend in terms of likes or number Of views."

        recommendations = []

        user = self.userManager.searchForUser(userForComparison.getId())

        usersWithSimilarInterests = self.userManager.getUsersWithSimilarHistories(user, 10, 100)

        if usersWithSimilarInterests is not list:
            return "Try recommendations based on number of likes"

        sortedListOfUsersWithSimilarInterests = self.userManager.getSortedListOfUsersBasedOnSimilarity(usersWithSimilarInterests, 100)

        for similarUser in sortedListOfUsersWithSimilarInterests:
            for history in similarUser.getHistory():
                if history not in recommendations:
                    recommendations.append(history)

        for history in recommendations:
            for historyOfUser in userForComparison.getHistory():
                if history[1] == historyOfUser[1]:
                    recommendations.remove(history)

        if len(recommendations) > maximumRecommendations:
            return recommendations[:maximumRecommendations]
        
        else:
            return recommendations
        
    def recommendationsBasedOnNumberOfLikes(self, maximum = 10):
        recommendations = []

        records = self.storageEngine.getAllRecords()

        filteredRecords = self.filter.getRecordsWithLabel("NumberOfLikes",records)

        sortedFilteredRecords = self.filter.sortRecords(filteredRecords, "NumberOfLikes")

        recommendations = sortedFilteredRecords

        if len(recommendations) < maximum:
            return recommendations
        
        else:
            return recommendations[:maximum]
        
    def recommendationsBasedOnNumberOfViews(self, maximum = 10):
        recommendations = []

        records = self.storageEngine.getAllRecords()

        filteredRecords = self.filter.getRecordsWithLabel("NumberOfViews",records)

        sortedFilteredRecords = self.filter.sortRecords(filteredRecords, "NumberOfViews")

        recommendations = sortedFilteredRecords

        if len(recommendations) < maximum:
            return recommendations
        
        else:
            return recommendations[:maximum]
        
    def recommendationsBasedOnCategory(self, category:str, maximum = 10):

        recommendations = self.recommendationsBasedOnNumberOfViews(100)
        rawdata = self.storageEngine.getRecordsInCategory(category)

        if rawdata == "Category Doesn't exist":
            return "Category Doesn't exist"

        recommendationFinalList = []

        for recommendation in recommendations:
            for rawdatapoint in rawdata:
                if recommendation.keys()[0] == rawdatapoint.keys()[0]:
                    recommendationFinalList.append(recommendation)

        return recommendationFinalList
    
    def recommendationBasedOnLocation(self, location:Location, rangeInMeters:str=None, maximumRecommendations = 10):

        users = None
        recommendations = []
        recommendationsDetailed = []

        if rangeInMeters is None:
            users = self.userManager.getUsersInRangeOfLocation(10000, location=location)

        else:
            users = self.userManager.getUsersInRangeOfLocation(meters=rangeInMeters, location=location)

        for user in users:
            for history in user.getHistory():
                if history not in recommendations:
                    recommendations.append(history)

        for recommendation in recommendations:
            if self.storageEngine.getRecordWithId(recommendation[1]) is str:
                recommendationsDetailed.append(self.storageEngine.getRecordWithId(recommendation[1]))

        return recommendationsDetailed
            






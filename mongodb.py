import collections
import pymongo

class mongodbconnection:
    #this class shall be used for mongodb connection
    def __init__(self, username, password):
        try:
            self.username = username
            self.password = password
            self.url = f"mongodb+srv://username:password@sahilclmongo05102022.slf44ij.mongodb.net/?retryWrites=true&w=majority"
        except Exception as e:
            raise e


    def getMongoClient(self):
        # It creates the connection with the database
        try:
            client = pymongo.MongoClient(self.url)
            return client
        except Exception as e:
            raise e

    
    def getDatabase(self, dbName):
        # Give Database 
        try:
            client = self.getMongoClient()
            database = client[dbName]
            return database
        except Exception as e:
            raise e

    
    def getCollection(self, dbName, collectionName):
        # Gives collection of a database
        try:
            database = self.getDatabase(dbName)
            collection = database[collectionName]
            return collection
        except Exception as e:
            raise e


    def isDatabasePresent(self, dbName):
        # Checks whether database is present
        try:
            client = self.getMongoClient()
            if dbName in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise e


    def isCollectionPresent(self, dbName, collectionName):
        # Checks whether the collection is present
        try:
            if self.isDatabasePresent(dbName):
                database  = self.getDatabase(dbName)
                if collectionName in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise e
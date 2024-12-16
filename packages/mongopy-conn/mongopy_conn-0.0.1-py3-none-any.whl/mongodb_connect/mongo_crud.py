from typing import Any 
import os
import pandas as pd
import pymongo 
import json
from ensure import ensure_annotations

from typing import Any
import os
import pandas as pd
from pymongo.mongo_client import MongoClient
import json
from ensure import ensure_annotations



class MongoDBOperation:
    """ 
    MongoDB operations for a given database and collection.
    PARAMETERS:
    client_url : the client url
    database_name (str): Name of the database
    collection_name (str): Name of the collection to perform operations on.
    """
    __collection = None # a variable that will be storing the collection name
    __database = None # a variable that will be storing the database name

    def __init__(self,client_url: str, database_name: str, collection_name: str=None):
        self.client_url=client_url
        self.database_name=database_name
        self.collection_name=collection_name
       
    def create_mongo_client(self,collection=None):
        client=MongoClient(self.client_url)
        return client
    
    def create_database(self,collection=None):
        if MongoDBOperation.__database==None:
            client=self.create_mongo_client(collection)
            self.database=client[self.database_name]
        return self.database 
    
    def create_collection(self,collection=None):
        if MongoDBOperation.__collection==None:
            database=self.create_database(collection)
            self.collection=database[self.collection_name]
            MongoDBOperation.__collection=collection
        
        if MongoDBOperation.__collection!=collection:
            database=self.create_database(collection)
            self.collection=database[self.collection_name]
            MongoDBOperation.__collection=collection
            
        return self.collection
    
    def insert_record(self,record: dict, collection_name: str) -> Any:
        if type(record) == list:
            for data in record:
                if type(data) != dict:
                    raise TypeError("record must be in the dict")    
            collection=self.create_collection(collection_name)
            collection.insert_many(record)
        elif type(record)==dict:
            collection=self.create_collection(collection_name)
            collection.insert_one(record)
    
    def bulk_insert(self,datafile,collection_name:str=None):
        self.path=datafile
        
        if self.path.endswith('.csv'):
            pd.read.csv(self.path,encoding='utf-8')
            
        elif self.path.endswith(".xlsx"):
            dataframe=pd.read_excel(self.path,encoding='utf-8')
            
        datajson=json.loads(dataframe.to_json(orient='record'))
        collection=self.create_collection()
        collection.insert_many(datajson)

    def find_one(self,collection_name:str,query:dict=None):
        collection=self.create_collection(collection_name)
        return collection.find_one(query)
    

    def find_all(self,collection_name:str,query:dict=None):
        # collection=self.create_collection(collection_name)
        if query:
            return self.create_collection(collection_name).find(query)
        else:
            return self.create_collection(collection_name).find()
        
    def update(self,collection_name:str,query:dict,new_values:dict):
        collection=self.create_collection(collection_name)
        collection.update_one(query, new_values)

    def delete(self,collection_name:str,query:dict):
        collection=self.create_collection(collection_name)
        collection.delete_one(query)

    
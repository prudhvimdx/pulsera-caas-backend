# # from flask_pymongo import PyMongo
# from bson import ObjectId

# class MongoDBManager:
#     def __init__(self, db, collection_name):
#         self.collection = db[collection_name]

#     def insert(self, data):
#         return self.collection.insert_one(data).inserted_id

#     def insert_many(self, data_list):
#         return self.collection.insert_many(data_list).inserted_ids

#     def find_by_id(self, id):
#         return self.collection.find_one({"_id": ObjectId(id)})

#     def find(self, query):
#         return list(self.collection.find(query))

#     def update(self, id, data):
#         return self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})

#     def update_many(self, query, data):
#         return self.collection.update_many(query, {"$set": data})

#     def delete(self, id):
#         return self.collection.delete_one({"_id": ObjectId(id)})

#     def delete_many(self, query):
#         return self.collection.delete_many(query)
    
#     def run_aggregation(self, query):
#         # Here query is an array
#         return list(self.collection.aggregate(query))
    
    
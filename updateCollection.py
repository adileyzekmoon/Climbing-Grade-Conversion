from pymongo import MongoClient
from trueskill import Rating, rate_1vs1

defaultMu = 100
defaultSigma = 33

client = MongoClient('mongodb+srv://adileyzekmoon:baozakeruga@cluster0.tnqbh.mongodb.net/ClimbingConversion?retryWrites=true&w=majority')

db = client.ClimbingConversionDB

collection = db.conversionCollectionV1

post = collection.find_one_and_update({"name": "Climbing Conversion Grades"},
                                     {"$setOnInsert": {"grades":{"test":"test successful"              
                                                         
                                                        }
                                              }
                                     }
                                     )
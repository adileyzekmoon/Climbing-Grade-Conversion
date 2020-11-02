from pymongo import MongoClient
from trueskill import Rating, rate_1vs1

defaultMu = 25

client = MongoClient('mongodb+srv://adileyzekmoon:baozakeruga@cluster0.tnqbh.mongodb.net/ClimbingConversion?retryWrites=true&w=majority')

db = client.ClimbingConversionDB

collection = db.conversionCollection

post = collection.find_one_and_update({"name": "Climbing Conversion Grades"},
                                     {"$set": {"grades.testGrade1" : defaultMu}})
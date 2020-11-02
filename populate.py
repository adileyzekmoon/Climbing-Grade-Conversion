from pymongo import MongoClient
from trueskill import Rating, rate_1vs1

defaultMu = 100

client = MongoClient('mongodb+srv://adileyzekmoon:baozakeruga@cluster0.tnqbh.mongodb.net/ClimbingConversion?retryWrites=true&w=majority')

db = client.ClimbingConversionDB

collection = db.conversionCollection

testData = {"name": "Climbing Conversion Grades",
            "dataCount": 0,
            "grades":{"Onsight Climbing Gym - Black" : defaultMu,
                      "Onsight Climbing Gym - Pink" : defaultMu,
                      "Onsight Climbing Gym - Lime" : defaultMu,
                      "Onsight Climbing Gym - Red" : defaultMu, 
                      "Onsight Climbing Gym - Green" : defaultMu, 
                      "Onsight Climbing Gym - Orange" : defaultMu, 
                      "Onsight Climbing Gym - Blue" : defaultMu, 
                      "Onsight Climbing Gym - White" : defaultMu, 
                      "Onsight Climbing Gym - Yellow" : defaultMu,
                      "Boulder World - Pink": defaultMu,
                      "Boulder World - Purple": defaultMu,
                      "Boulder World - Lime": defaultMu,
                      "Boulder World - Orange": defaultMu,
                      "Boulder World - White": defaultMu,
                      "Boulder World - Red": defaultMu,
                      "Boulder World - Yellow": defaultMu,
                      "Boulder World - Blue": defaultMu,
                      "Boulder Plus - White": defaultMu,
                      "Boulder Plus - Yellow": defaultMu,
                      "Boulder Plus - Red": defaultMu,
                      "Boulder Plus - Blue": defaultMu,
                      "Boulder Plus - Purple": defaultMu,
                      "Boulder Plus - Green": defaultMu,
                      "Boulder Plus - Pink": defaultMu,
                      "Lighthouse - Level 1": defaultMu,
                      "Lighthouse - Level 2": defaultMu,
                      "Lighthouse - Level 3": defaultMu,
                      "Lighthouse - Level 4": defaultMu,
                      "Lighthouse - Level 5": defaultMu,
                      "Lighthouse - Level 6": defaultMu,
                      "Lighthouse - Level 7": defaultMu,
                      "Lighthouse - Level 8": defaultMu,
                      "Lighthouse - Level 9": defaultMu
                      
                     }}

post = collection.insert_one(testData)

#result = collection.find_one({"name": "Onsight Climbing Gym"})

#print(result["grades"]["black"])
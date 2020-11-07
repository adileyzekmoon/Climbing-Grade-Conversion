from pymongo import MongoClient
from trueskill import Rating, rate_1vs1

defaultMu = 100
defaultSigma = 33

client = MongoClient('mongodb+srv://adileyzekmoon:baozakeruga@cluster0.tnqbh.mongodb.net/ClimbingConversionDB?retryWrites=true&w=majority')

db = client.ClimbingConversionDB

collection = db.conversionCollectionV1

testData = {"name": "Climbing Conversion Grades",
            "dataCount": 0,
            "grades":{"Onsight Climbing - Black" : [defaultMu, defaultSigma],
                      "Onsight Climbing - Pink" : [defaultMu, defaultSigma],
                      "Onsight Climbing - Lime" : [defaultMu, defaultSigma],
                      "Onsight Climbing - Red" : [defaultMu, defaultSigma],
                      "Onsight Climbing - Purple" : [defaultMu, defaultSigma],
                      "Onsight Climbing - Green" : [defaultMu, defaultSigma], 
                      "Onsight Climbing - Orange" : [defaultMu, defaultSigma], 
                      "Onsight Climbing - Blue" : [defaultMu, defaultSigma], 
                      "Onsight Climbing - White" : [defaultMu, defaultSigma], 
                      "Onsight Climbing - Yellow" : [defaultMu, defaultSigma],
                      "Boulder World - Pink": [defaultMu, defaultSigma],
                      "Boulder World - Purple": [defaultMu, defaultSigma],
                      "Boulder World - Lime": [defaultMu, defaultSigma],
                      "Boulder World - Orange": [defaultMu, defaultSigma],
                      "Boulder World - White": [defaultMu, defaultSigma],
                      "Boulder World - Red": [defaultMu, defaultSigma],
                      "Boulder World - Yellow": [defaultMu, defaultSigma],
                      "Boulder World - Blue": [defaultMu, defaultSigma],
                      "Boulder Plus - White": [defaultMu, defaultSigma],
                      "Boulder Plus - Yellow": [defaultMu, defaultSigma],
                      "Boulder Plus - Red": [defaultMu, defaultSigma],
                      "Boulder Plus - Blue": [defaultMu, defaultSigma],
                      "Boulder Plus - Purple": [defaultMu, defaultSigma],
                      "Boulder Plus - Green": [defaultMu, defaultSigma],
                      "Boulder Plus - Pink": [defaultMu, defaultSigma],
                      "Lighthouse - Level 1": [defaultMu, defaultSigma],
                      "Lighthouse - Level 2": [defaultMu, defaultSigma],
                      "Lighthouse - Level 3": [defaultMu, defaultSigma],
                      "Lighthouse - Level 4": [defaultMu, defaultSigma],
                      "Lighthouse - Level 5": [defaultMu, defaultSigma],
                      "Lighthouse - Level 6": [defaultMu, defaultSigma],
                      "Lighthouse - Level 7": [defaultMu, defaultSigma],
                      "Lighthouse - Level 8": [defaultMu, defaultSigma],
                      "Lighthouse - Level 9": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 0": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 1": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 2": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 3": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 4": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 5": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 6": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 7": [defaultMu, defaultSigma],
                      "Fit Bloc - Level 8": [defaultMu, defaultSigma],
                      "Climb Central - Level 1": [defaultMu, defaultSigma],
                      "Climb Central - Level 2": [defaultMu, defaultSigma],
                      "Climb Central - Level 3": [defaultMu, defaultSigma],
                      "Climb Central - Level 4": [defaultMu, defaultSigma],
                      "Climb Central - Level 5": [defaultMu, defaultSigma],
                      "Climb Central - Level 6": [defaultMu, defaultSigma],
                      "BFF Climb - Level 1": [defaultMu, defaultSigma],
                      "BFF Climb - Level 2": [defaultMu, defaultSigma],
                      "BFF Climb - Level 3": [defaultMu, defaultSigma],
                      "BFF Climb - Level 4": [defaultMu, defaultSigma],
                      "BFF Climb - Level 5": [defaultMu, defaultSigma],
                      "BFF Climb - Level 6": [defaultMu, defaultSigma],
                      "BFF Climb - Level 7": [defaultMu, defaultSigma],
                      "BFF Climb - Level 8": [defaultMu, defaultSigma],
                      "BFF Climb - Level 9": [defaultMu, defaultSigma],
                      "BFF Climb - Level 10": [defaultMu, defaultSigma],
                      "BFF Climb - Level 11": [defaultMu, defaultSigma],
                      "BFF Climb - Level 12": [defaultMu, defaultSigma],
                      "Ground Up - Brown": [defaultMu, defaultSigma],
                      "Ground Up - Pink": [defaultMu, defaultSigma],
                      "Ground Up - Red": [defaultMu, defaultSigma],
                      "Ground Up - Orange": [defaultMu, defaultSigma],
                      "Ground Up - Yellow": [defaultMu, defaultSigma],
                      "Ground Up - Green": [defaultMu, defaultSigma],
                      "Ground Up - Light Blue": [defaultMu, defaultSigma],
                      "Ground Up - Dark Blue": [defaultMu, defaultSigma],
                      "Ground Up - Grey": [defaultMu, defaultSigma],
                      "Ground Up - Black": [defaultMu, defaultSigma],
                      "Kinetics - White": [defaultMu, defaultSigma],
                      "Kinetics - Red": [defaultMu, defaultSigma],
                      "Kinetics - Blue": [defaultMu, defaultSigma],
                      "Kinetics - Yellow": [defaultMu, defaultSigma],
                      "Kinetics - Green": [defaultMu, defaultSigma]                     
                      
                     }}

post = collection.insert_one(testData)

#result = collection.find_one({"name": "Onsight Climbing Gym"})

#print(result["grades"]["black"])
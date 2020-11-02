from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from trueskill import Rating, rate_1vs1
import random

client = MongoClient('mongodb+srv://adileyzekmoon:baozakeruga@cluster0.tnqbh.mongodb.net/ClimbingConversion?retryWrites=true&w=majority')

db = client.ClimbingConversionDB

collection = db.conversionCollection

app = Flask(__name__)

@app.route('/')
def main():
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    grades = list(gym["grades"].keys())
    contenders = random.sample(grades, 2)
    gradeA = contenders[0]
    gradeB = contenders[1]
    dataCount = gym["dataCount"]
    
#    print(gym)
    
    return render_template('index.html', gradeA=gradeA, gradeB=gradeB, dataCount=dataCount)

@app.route('/submit', methods=["POST", "GET"])
def submit():
    winner = request.args.get("winner")
    loser = request.args.get("loser")
    print(winner)
    print(loser)
    
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    dataCount = gym["dataCount"]
    
    winnerRating, loserRating = rate_1vs1(Rating(gym["grades"][winner]), Rating(gym["grades"][loser]))
    print(winnerRating.mu)
    print(loserRating.mu)
    
    post = collection.find_one_and_update({"name": "Climbing Conversion Grades"},
                                          {"$set": {"grades."+winner : winnerRating.mu,
                                                    "grades."+loser : loserRating.mu},
                                          "$inc": {"dataCount": 1}
                                          }
                                         )

    grades = list(gym["grades"].keys())
    contenders = random.sample(grades, 2)
    gradeA = contenders[0]
    gradeB = contenders[1]
#    print(gym)
    
    return redirect(url_for('main'))


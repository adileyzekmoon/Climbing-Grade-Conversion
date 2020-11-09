from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from trueskill import Rating, rate_1vs1
import random
from db import client
import os

boulderGyms = ["Onsight Climbing", "Boulder World", "Lighthouse", "Boulder Plus", "Fit Bloc", "Climb Central", "BFF Climb", "Ground Up", "Kinetics"]
gymImg = ["OS.png", "BW.png", "LH.png", "BP.webp", "FB.png", "CC.png", "BFF.png", "GU.png", "K.png"]

db = client.ClimbingConversionDB

collection = db.conversionCollectionV1

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def main():
    
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    grades = list(gym["grades"].keys())
    userGymList = []
    completeGymList = boulderGyms
    
    if ((request.method == 'POST') and (len(request.form.getlist("gyms"))>0)) :
        print(request.form.getlist("gyms"))
        
        #if one of the 2 submit buttons were pressed
        if (request.form["result"] != "SKIP" ):
            print(request.form["result"])
            print(type(request.form["result"]))
            splitResult = request.form["result"].split(",")
            print(splitResult)
            winner, loser = [splitResult[0][2:-1], splitResult[1][2:-2]]
            print(winner)
            print(loser)
            
            dataCount = gym["dataCount"]
            
            #before matchup
            winnerRating = Rating(gym["grades"][winner][0],gym["grades"][winner][1])
            loserRating = Rating(gym["grades"][loser][0],gym["grades"][winner][1])
            
            #after matchup
            winnerRating, loserRating = rate_1vs1(winnerRating, loserRating)
            print(winnerRating)
            print(loserRating)
            
            post = collection.find_one_and_update({"name": "Climbing Conversion Grades"},
                                                  {"$set": {"grades."+winner : [winnerRating.mu, 
                                                                                winnerRating.sigma],
                                                            "grades."+loser : [loserRating.mu, 
                                                                               loserRating.sigma]},
                                                   "$inc": {"dataCount": 1}
                                                  }
                                                 )
        
        userGymList = request.form.getlist("gyms")
        contenderList = []
        for eachGrade in grades:
            for eachGym in userGymList:
                if (eachGym in eachGrade):
                    contenderList.append(eachGrade)
                    
        #        print(contenderList)
        contenders = random.sample(contenderList, 2)
        
        ratingDiff = abs(gym["grades"][contenders[0]][0] - gym["grades"][contenders[1]][0]) 
        print(ratingDiff, contenders[0], contenders[1])
        while (ratingDiff > 30):
            #keep the one with fewer past matchups
            if (gym["grades"][contenders[0]][1] > gym["grades"][contenders[1]][1]):
                contenders[1] = random.choice(contenderList)
                ratingDiff = abs(gym["grades"][contenders[0]][0] - gym["grades"][contenders[1]][0])
                print(ratingDiff, contenders[0], contenders[1])
            else:
                contenders[0] = random.choice(contenderList)
                ratingDiff = abs(gym["grades"][contenders[0]][0] - gym["grades"][contenders[1]][0])
                print(ratingDiff, contenders[0], contenders[1])
        
    else:        
        userGymList = boulderGyms
        contenders = random.sample(grades, 2)
        ratingDiff = abs(gym["grades"][contenders[0]][0] - gym["grades"][contenders[1]][0]) 
        print(ratingDiff, contenders[0], contenders[1])
        while (ratingDiff > 30):
            #keep the one with fewer past matchups
            if (gym["grades"][contenders[0]][1] > gym["grades"][contenders[1]][1]):
                contenders[1] = random.choice(grades)
                ratingDiff = abs(gym["grades"][contenders[0]][0] - gym["grades"][contenders[1]][0])
                print(ratingDiff, contenders[0], contenders[1])
            else:
                contenders[0] = random.choice(grades)
                ratingDiff = abs(gym["grades"][contenders[0]][0] - gym["grades"][contenders[1]][0])
                print(ratingDiff, contenders[0], contenders[1])
        
        
    gradeA = contenders[0]
    gradeB = contenders[1]
    dataCount = gym["dataCount"]
        
    for i in range(len(boulderGyms)):
        if boulderGyms[i] in gradeA:
            imageA = gymImg[i]
            
    for i in range(len(boulderGyms)):
        if boulderGyms[i] in gradeB:
            imageB = gymImg[i]
    
#    print(gym)
#    print(userGymList)
#    print(completeGymList)
    return render_template('index.html', gradeA=gradeA, gradeB=gradeB, dataCount=dataCount, imageA=imageA, imageB=imageB, userGymList=userGymList, completeGymList=completeGymList)

@app.route('/submit', methods=["POST", "GET"])
def submit():
    winner = request.args.get("winner")
    loser = request.args.get("loser")
    print(winner)
    print(loser)
    
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    dataCount = gym["dataCount"]
    
    #before matchup
    winnerRating = Rating(gym["grades"][winner][0],gym["grades"][winner][1])
    loserRating = Rating(gym["grades"][loser][0],gym["grades"][winner][1])
    
    #after matchup
    winnerRating, loserRating = rate_1vs1(winnerRating, loserRating)
    print(winnerRating)
    print(loserRating)
    
    post = collection.find_one_and_update({"name": "Climbing Conversion Grades"},
                                          {"$set": {"grades."+winner : [winnerRating.mu, winnerRating.sigma],
                                                    "grades."+loser : [loserRating.mu, loserRating.sigma]},
                                          "$inc": {"dataCount": 1}
                                          }
                                         )

    grades = list(gym["grades"].keys())
    contenders = random.sample(grades, 2)
    gradeA = contenders[0]
    gradeB = contenders[1]
#    print(gym)
    
    return redirect(url_for('main'))


@app.route('/graph')
def graph():
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    grades = list(gym["grades"].keys())
    ratings = list(gym["grades"].values())
    dataCount = gym["dataCount"]
    os = []
    bw = []
    bp = []
    lh = []
    fb = []
    cc = []
    bff = []
    gu = []
    k=[]
    for i in range(len(grades)):
        if ("Onsight Climbing" in grades[i]):
            os.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
            
        if ("Boulder World" in grades[i]):
            bw.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
            
        if ("Boulder Plus" in grades[i]):
            bp.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
            
        if ("Lighthouse" in grades[i]):
            lh.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
            
        if ("Fit Bloc" in grades[i]):
            fb.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
            
        if ("Climb Central" in grades[i]):
            cc.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
            
        if ("BFF Climb" in grades[i]):
            bff.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
            
        if ("Ground Up" in grades[i]):
            gu.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
        
        if ("Kinetics" in grades[i]):
            k.append({"y": ratings[i][0],
                            "label": grades[i]
                           })
    
    
    
            
    
    
    return render_template('graph.html', dataCount=dataCount, os=os, bw=bw, bp=bp, lh=lh, fb=fb, cc=cc, bff=bff, gu=gu, k=k)


@app.route('/rangebar')
def rangebar():
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    grades = list(gym["grades"].keys())
    ratings = list(gym["grades"].values())
    dataCount = gym["dataCount"]
    os = []
    bw = []
    bp = []
    lh = []
    fb = []
    cc = []
    bff = []
    gu = []
    k=[]
    for i in range(len(grades)):
        if ("Onsight Climbing" in grades[i]):
            os.append(ratings[i][0])
            
        if ("Boulder World" in grades[i]):
            bw.append(ratings[i][0])
            
        if ("Boulder Plus" in grades[i]):
            bp.append(ratings[i][0])
            
        if ("Lighthouse" in grades[i]):
            lh.append(ratings[i][0])
            
        if ("Fit Bloc" in grades[i]):
            fb.append(ratings[i][0])
            
        if ("Climb Central" in grades[i]):
            cc.append(ratings[i][0])
            
        if ("BFF Climb" in grades[i]):
            bff.append(ratings[i][0])
            
        if ("Ground Up" in grades[i]):
            gu.append(ratings[i][0])
        
        if ("Kinetics" in grades[i]):
            k.append(ratings[i][0])
    
    os = [min(os), max(os)]
    bw = [min(bw), max(bw)]
    bp = [min(bp), max(bp)]
    lh = [min(lh), max(lh)]
    fb = [min(fb), max(fb)]
    cc = [min(cc), max(cc)]
    bff = [min(bff), max(bff)]
    gu = [min(gu), max(gu)]
    k=[min(k), max(k)]
    
    print(os)  
    
    return render_template('rangebar.html', dataCount=dataCount, os=os, bw=bw, bp=bp, lh=lh, fb=fb, cc=cc, bff=bff, gu=gu, k=k)


@app.route('/orderedbar')
def orderedbar():
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    sortedGyms = sorted(gym["grades"].items(), key=lambda x: x[1][0])
    
    data = [] 
    
    
    for i in range(len(sortedGyms)):
        data.append({"y": sortedGyms[i][1][0],
                            "label": sortedGyms[i][0]
                           })
    
#    print(data)
    
    return render_template('orderedbar.html', data=data)

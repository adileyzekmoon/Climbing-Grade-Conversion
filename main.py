from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from trueskill import Rating, rate_1vs1
import random
import statistics
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
        while ((ratingDiff > 30) or (contenders[0] == contenders[1])):
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
        while ((ratingDiff > 30) or (contenders[0] == contenders[1])):
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
    
#    print(os)  
    
    return render_template('rangebar.html', dataCount=dataCount, os=os, bw=bw, bp=bp, lh=lh, fb=fb, cc=cc, bff=bff, gu=gu, k=k)


@app.route('/orderedbar')
def orderedbar():
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    sortedGyms = sorted(gym["grades"].items(), key=lambda x: x[1][0])
    
    data = [] 
    
    
    for i in range(len(sortedGyms)):
        data.insert(0, {"y": round(sortedGyms[i][1][0], 2),
                            "label": sortedGyms[i][0]
                           })
    
#    print(data)
    
    return render_template('orderedbar.html', data=data)

@app.route('/scatter')
def scatter():
    gym = collection.find_one({"name": "Climbing Conversion Grades"})
    grades = list(gym["grades"].keys())
    ratings = list(gym["grades"].values())
    dataCount = gym["dataCount"]
    os = []
    osb = []
    bw = []
    bwb=[]
    bp = []
    lh = []
    fb = []
    cc = []
    bff = []
    gu = []
    k=[]
    bpb = []
    lhb = []
    fbb = []
    ccb = []
    bffb = []
    gub = []
    kb=[]
    for i in range(len(grades)):
        if ("Onsight Climbing" in grades[i]):
            os.append({"x": 1.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            osb.append(ratings[i][0])
            
        if ("Boulder World" in grades[i]):
            bw.append({"x": 2.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            bwb.append(ratings[i][0])
            
        if ("Boulder Plus" in grades[i]):
            bp.append({"x": 3.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            bpb.append(ratings[i][0])
            
        if ("Lighthouse" in grades[i]):
            lh.append({"x": 4.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            lhb.append(ratings[i][0])
            
        if ("Fit Bloc" in grades[i]):
            fb.append({"x": 5.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            fbb.append(ratings[i][0])
            
        if ("Climb Central" in grades[i]):
            cc.append({"x": 6.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            ccb.append(ratings[i][0])
            
        if ("BFF Climb" in grades[i]):
            bff.append({"x": 7.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            bffb.append(ratings[i][0])
            
        if ("Ground Up" in grades[i]):
            gu.append({"x": 8.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            gub.append(ratings[i][0])
        
        if ("Kinetics" in grades[i]):
            k.append({"x": 9.2,
                       "y": ratings[i][0],
                       "label": grades[i]})
            kb.append(ratings[i][0])

    
    
    osb = [min(osb),statistics.quantiles(osb)[0],statistics.quantiles(osb)[2], max(osb), statistics.quantiles(osb)[1]]
    bwb = [min(bwb),statistics.quantiles(bwb)[0],statistics.quantiles(bwb)[2], max(bwb), statistics.quantiles(bwb)[1]]
    bpb = [min(bpb),statistics.quantiles(bpb)[0],statistics.quantiles(bpb)[2], max(bpb), statistics.quantiles(bpb)[1]]
    lhb = [min(lhb),statistics.quantiles(lhb)[0],statistics.quantiles(lhb)[2], max(lhb), statistics.quantiles(lhb)[1]]
    fbb = [min(fbb),statistics.quantiles(fbb)[0],statistics.quantiles(fbb)[2], max(fbb), statistics.quantiles(fbb)[1]]
    ccb = [min(ccb),statistics.quantiles(ccb)[0],statistics.quantiles(ccb)[2], max(ccb), statistics.quantiles(ccb)[1]]
    bffb = [min(bffb),statistics.quantiles(bffb)[0],statistics.quantiles(bffb)[2], max(bffb), statistics.quantiles(bffb)[1]]
    gub = [min(gub),statistics.quantiles(gub)[0],statistics.quantiles(gub)[2], max(gub), statistics.quantiles(gub)[1]]
    kb = [min(kb),statistics.quantiles(kb)[0],statistics.quantiles(kb)[2], max(kb), statistics.quantiles(kb)[1]]

    
    return render_template('scatter.html', dataCount=dataCount, os=os, bw=bw, bp=bp, lh=lh, fb=fb, cc=cc, bff=bff, gu=gu, k=k, osb=osb, bwb=bwb, bpb=bpb, lhb=lhb, fbb=fbb, ccb=ccb, bffb=bffb, gub=gub, kb=kb)

@app.route('/conversion')
def conversion():
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
    for i in grades:
        if ("Onsight Climbing" in i):
            os.append(i)
            
        if ("Boulder World" in i):
            bw.append(i)
            
        if ("Boulder Plus" in i):
            bp.append(i)
            
        if ("Lighthouse" in i):
            lh.append(i)
            
        if ("Fit Bloc" in i):
            fb.append(i)
            
        if ("Climb Central" in i):
            cc.append(i)
            
        if ("BFF Climb" in i):
            bff.append(i)
            
        if ("Ground Up" in i):
            gu.append(i)
            
        if ("Kinetics" in i):
            k.append(i)
            
    return render_template('conversion.html', gym=gym, os=os, bw=bw, bp=bp, lh=lh, fb=fb, cc=cc, bff=bff, gu=gu, k=k)
        
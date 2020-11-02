from trueskill import Rating, rate_1vs1

grades = {"black" : Rating(),
          "red" : Rating(), 
          "green" : Rating(), 
          "orange" : Rating(), 
          "blue" : Rating()}

print(grades)
#red vs green
grades["green"], grades["red"] = rate_1vs1(grades["green"], grades["red"])


#green vs orange
grades["orange"], grades["green"] = rate_1vs1(grades["orange"], grades["green"])
#red vs orange
grades["orange"], grades["red"] = rate_1vs1(grades["orange"], grades["red"])
#red vs blue
grades["blue"], grades["red"] = rate_1vs1(grades["blue"], grades["red"])

#black vs red
grades["red"], grades["black"] = rate_1vs1(grades["red"], grades["black"])
#black vs green
grades["green"], grades["black"] = rate_1vs1(grades["green"], grades["black"])
#black vs orange
grades["orange"], grades["black"] = rate_1vs1(grades["orange"], grades["black"])



#green vs blue
grades["blue"], grades["green"] = rate_1vs1(grades["blue"], grades["green"])
#black vs blue
grades["blue"], grades["black"] = rate_1vs1(grades["blue"], grades["black"])
#orange vs blue
grades["blue"], grades["orange"] = rate_1vs1(grades["blue"], grades["orange"])

print(grades)
print(grades["blue"].mu)
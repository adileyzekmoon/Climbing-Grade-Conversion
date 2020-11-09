from trueskill import Rating, rate_1vs1

testA = Rating(100,33)
testB = Rating(100,20)

print(testA,testB)

testA, testB = rate_1vs1(testA, testB)

print(testA,testB)
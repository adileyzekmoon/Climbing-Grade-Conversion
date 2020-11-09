from trueskill import Rating, rate_1vs1

testA = Rating(100,33)
testB = Rating(100,1)
testC = Rating(10,33)
testD = Rating(10,1)

a = "100,new / "
b = "100,old / "
c = "10,new / "
d = "10,old / "

print(a+a)
print(rate_1vs1(testA, testA))

print(b+b)
print(rate_1vs1(testB, testB))

print(c+c)
print(rate_1vs1(testC, testC))

print(d+d)
print(rate_1vs1(testD, testD))

print(a+b)
print(rate_1vs1(testA, testB))

print(b+a)
print(rate_1vs1(testB, testA))

print(a+c)
print(rate_1vs1(testA, testC))

print(c+a)
print(rate_1vs1(testC, testA))

print(a+d)
print(rate_1vs1(testA, testD))

print(d+a)
print(rate_1vs1(testD, testA))

print(b+c)
print(rate_1vs1(testB, testC))

print(c+b)
print(rate_1vs1(testC, testB))

print(b+d)
print(rate_1vs1(testB, testD))

print(d+b)
print(rate_1vs1(testD, testB))

print(c+d)
print(rate_1vs1(testC, testD))

print(d+c)
print(rate_1vs1(testD, testC))

myDict = {}

def myFunc(data):
    data["key"] = "abc"

myDict["key"] = None

print(myDict["key"])

myFunc(myDict)
print(myDict["key"])


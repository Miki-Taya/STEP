from collections import defaultdict
from collections import deque

def readTextToList(text):
    list = []
    for line in open(text,"r"):
        temp_list = line[:-1].split("\t")
        list.append(tuple(temp_list))
    return list

def scanFromTo():
    print("from : ", end = '')
    fromName = input()
    print("to : ", end = '')
    toName = input()
    return fromName, toName

def makeDict(followData):
    index = 0
    followDict = defaultdict(list)
    for i in range(len(followData)):
        followDict[followData[i][0]].append(followData[i][1])
    return followDict

def getStep(nameData, followData, followDict, fromName, toName):
    pendingNodes = deque([])
    checkList = []
    countList =[]
    counter = 0
    judgeFrom = 0
    judgeTo = 0
    fromIndex = 0
    toIndex = 0
    for Tuple in nameData:
        print(fromName in Tuple)
        if fromName in Tuple == True:
            judgeFrom = fromName in Tuple
            print(judgeFrom)
            fromIndex = int(Tuple[0])
            break
    for Tuple in nameData:
        if toName in Tuple == True:
            judgeTo = toName in Tuple
            print(judgeTo)
            toIndex = int(Tuple[0])
            break
    fromNumber = nameData[fromIndex][0]
    toNumber = nameData[toIndex][0]
    countList.append(toNumber)
    if (judgeFrom == 1) and (judgeTo == 1):
        pendingNodes.append(fromNumber)
        while len(pendingNodes) > 0:
            pendingNodesContent = pendingNodes.popleft()
            if pendingNodesContent == toNumber:
                return counter
            elif pendingNodesContent not in checkList:
                checkList.append(pendingNodesContent)
                dictContent = followDict[str(pendingNodesContent)]
                pendingNodes.extend(dictContent)
                if pendingNodesContent in countList:
                    countList.append(dictContent[-1])
                    counter += 1
            elif len(pendingNode) == 0:
                print("Oh, not connecting from", nameData[fromIndex][1], "to", nameData[toIndex][1])
                break
    elif (judgeFrom == 0) and (judgeTo == 0):
        print(nameData[fromIndex][1], "and", nameData[toIndex][1], "are not in nicknames list.")
    elif (judgeFrom == 0) and (judgeTo == 1):
        print(nameData[fromIndex][1], "is not in nicknames list.")
    else:
        print(nameData[toIndex][1], "is not in nicknames list.")

def test(fromName, toName):
    followData = readTextToList("links.txt")
    nameData = readTextToList("nicknames.txt")
    followDict = makeDict(followData)
    counter = getStep(nameData, followData, followDict, fromName, toName)
    print(counter)

def runTest():
    print("==== Test started! ====")
    test('jacob', 'amy')
    test('jacob', 'billy')
    test('jacob', 'karl')
    print("==== Test finished! ====\n")

runTest()


followData = readTextToList("links.txt")
nameData = readTextToList("nicknames.txt")
followDict = makeDict(followData)
(fromName, toName) = scanFromTo()
counter = getStep(nameData, followData, followDict, fromName, toName)
print(counter)

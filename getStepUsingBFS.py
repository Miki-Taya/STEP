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

def judgeInputAndGetIndex(nameData, input):
    judge = 0
    inputIndex = 0
    for Tuple in nameData:
        index, name = Tuple
        if name == input or index == input: #admit the input of name and index.
            judge = True
            inputIndex = index
            break
    return judge, inputIndex

def getStep(nameData, followData, followDict, fromInput, toInput):
    pendingNodes = deque([])
    checkList = []
    countList =[]
    counter = 0
    judgeFrom = 0
    judgeTo = 0
    fromIndex = 0
    toIndex = 0
    (judgeFrom, fromIndex) = judgeInputAndGetIndex(nameData, fromInput)
    (judgeTo, toIndex) = judgeInputAndGetIndex(nameData, toInput)
    countList.append(fromIndex)
    if (judgeFrom == 1) and (judgeTo == 1):
        pendingNodes.append(fromIndex)
        while len(pendingNodes) > 0:
            pendingNodesContent = pendingNodes.popleft()
            if pendingNodesContent == toIndex:
                return counter
            elif pendingNodesContent not in checkList:
                checkList.append(pendingNodesContent)
                dictContent = followDict[pendingNodesContent]
                pendingNodes.extend(dictContent)
                if pendingNodesContent in countList:  # for count step.
                    countList.append(dictContent[-1])
                    counter += 1
            elif len(pendingNodes) == 0:
                print("Oh, not connecting from", fromInput, "to", toInput)
                break
    elif (judgeFrom == 0) and (judgeTo == 0):
        print(fromInput, "and", toInput, "are not in nicknames list.")
    elif (judgeFrom == 0) and (judgeTo == 1):
        print(fromInput, "is not in nicknames list.")
    else:
        print(toInput, "is not in nicknames list.")

def test(fromInput, toInput):
    followData = readTextToList("links.txt")
    nameData = readTextToList("nicknames.txt")
    followDict = makeDict(followData)
    counter = getStep(nameData, followData, followDict, fromInput, toInput)
    if counter != None:
        print(counter)

def runTest():
    print("==== Test started! ====")
    test("jacob", "amy")
    test("jacob", "billy")
    test("jacob", "karl")
    print("==== Test finished! ====\n")

runTest()


followData = readTextToList("links.txt")
nameData = readTextToList("nicknames.txt")
followDict = makeDict(followData)
(fromInput, toInput) = scanFromTo()
counter = getStep(nameData, followData, followDict, fromInput, toInput)
if counter != None:
    print(counter)

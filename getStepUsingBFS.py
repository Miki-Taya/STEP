from collections import defaultdict
import queue

def readTextToList(text):
    list = []
    for line in open(text,"r"):
        list += line[:-1].split("\t")
    return list

def scanFromTo():
    print("from:")
    fromName = input()
    print("to:")
    toName = input()
    return fromName, toName

def makeDict(followData):
    index = 0
    followDict = defaultdict(list)
    while index < len(followData) - 1:
        followDict[followData[index]].append(followData[index + 1])
        index += 2
    return followDict

def getStep(nameData, followData, followDict):
    q = queue.Queue()
    checkList = []
    counter = 0
    (fromName, toName) = scanFromTo()
    if (fromName in nameData) and (toName in nameData):
        q.put(nameData[nameData.index(fromName)-1])
        q.put('*')
        quitCounter = 0
        while quitCounter >= 0:  # If there are consective `*`, quit repeating.
            qContent = q.get()
            if qContent == nameData[nameData.index(toName)-1]:
                print(counter, "STEP!!")
                break
            elif qContent == '*':
                quitCounter -= 1
                q.put('*')
                counter += 1
            elif not(qContent in checkList):
                quitCounter = 1
                checkList.append(qContent)
                for  followingnumber in followDict[str(qContent)]:
                    q.put(followingnumber)
        if quitCounter == -1:
                        print("Oh, not connecting from", fromName, "to", toName)
    elif not(fromName in nameData) and not(toName in nameData):
        print(fromName, "and", toName, "are not in nicknames list.")
    elif not(fromName in nameData):
        print(fromName, "is not in nicknames list.")
    else:
        print(toName, "is not in nicknames list.")



followData = readTextToList("links.txt")
nameData = readTextToList("nicknames.txt")
followDict = makeDict(followData)
getStep(nameData, followData, followDict)

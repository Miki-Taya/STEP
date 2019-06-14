def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def readTimes(line, index):
  token = {'type': 'TIMES'}
  return token, index + 1


def readDivide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1


def readRightPar(line, index):
  token = {'type': 'RIGHTPAR'}
  return token, index + 1


def readLeftPar(line, index):
  token = {'type': 'LEFTPAR'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readTimes(line, index)
    elif line[index] == '/':
      (token, index) = readDivide(line, index)
    elif line[index] == ')':
      (token, index) = readRightPar(line, index)
    elif line[index] == '(':
      (token, index) = readLeftPar(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def calculateTimesDivide(tokens):
  index = 1
  while index < len(tokens) - 1:
      if tokens[index]['type'] == 'NUMBER':
          if tokens[index + 1]['type'] == 'TIMES':
              answerTimes = tokens[index]['number'] * tokens[index + 2]['number']
              tokens.insert(index, {'type':'NUMBER','number':answerTimes})
              del tokens[index + 1 : index + 4]
          elif tokens[index + 1]['type'] == 'DIVIDE':
              answerDivide = tokens[index]['number'] / tokens[index + 2]['number']
              tokens.insert(index, {'type':'NUMBER','number':answerDivide})
              del tokens[index + 1 : index + 4]
          else:
              index += 1
      else:
          index += 1
  return tokens


def calculatePlusMinus(tokens):
  index = 1
  answer = 0
  while index < len(tokens):
      if tokens[index]['type'] == 'NUMBER':
          if tokens[index - 1]['type'] == 'PLUS':
              answer += tokens[index]['number']
          elif tokens[index - 1]['type'] == 'MINUS':
              answer -= tokens[index]['number']
          else:
              print('Invalid syntax')
              exit(1)
      index += 1
  return answer


def processNegativeNumber(tokens):
    index = 1
    while index < len(tokens) - 1:
        if tokens[index]['type'] == 'MINUS':
            if tokens[index - 1]['type'] == 'TIMES' or tokens[index - 1]['type'] == 'DIVIDE': #for example, 5*-1 change to -5*1.
                del tokens[index]
                tokens.insert(index - 2, {'type','MINUS'})
            elif tokens[index - 1]['type'] == 'PLUS': #for example, 5+-1 change to 5-1.
                del tokens[index]
        index +=1
    return tokens


def evaluate(tokens):
    tokens = processNegativeNumber(tokens)
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens = calculateTimesDivide(tokens)
    answer = calculatePlusMinus(tokens)
    return answer

def readLeftParIndexAndParCounter(tokens):
    index = 0
    leftParIndex = 0
    parCounter = 0
    while index < len(tokens):    #get the parCounter and the index of the most right "(".
        if tokens[index]['type'] == 'LEFTPAR':
            leftParIndex = index
            parCounter += 1
            index += 1
        else:
            index += 1
    return leftParIndex , parCounter


def readRightParIndex(tokens , leftParIndex):
    rightParIndex = 0
    index = leftParIndex + 4      #for example, the minimum size (3+4) show that ")" is fourth right of "(".
    while index < len(tokens):  #get the index of the most left ")".
        if tokens[index]['type'] == 'RIGHTPAR':
            rightParIndex = index
            break
        else:
            index += 1
    return rightParIndex


def deletePar(tokens , leftParIndex):
    if leftParIndex + 3 <len(tokens):
        if tokens[leftParIndex + 3]['type'] == 'RIGHTPAR':  #for example, 2*(-3) change to 2*-3.
            del tokens[leftParIndex]
            del tokens[leftParIndex + 2]
    return tokens


def evaluateParentheses(tokens):        #defeat parentheses.
  index = 0
  parCounter = 0
  leftParIndex = 0
  rightParIndex = 0
  (leftParIndex , parCounter) = readLeftParIndexAndParCounter(tokens)
  rightParIndex = readRightParIndex(tokens , leftParIndex)
  tokens = deletePar(tokens , leftParIndex)
  if parCounter == 0:       #until becoming parCounter==0, repeat parenthesesEvaluate and defeat parentheses.
      return tokens
  else:
      par = tokens[leftParIndex + 1 : rightParIndex]
      del tokens[leftParIndex : rightParIndex + 1]
      tokens.insert(leftParIndex , {'type':'NUMBER','number':evaluate(par)})    #defeat one parentheses.
      evaluateParentheses(tokens)
      return evaluateParentheses(tokens)


def test(line):
  tokens = tokenize(line)
  tokens = evaluateParentheses(tokens)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")

  test("2+3")
  test("2-3")
  test("2*3")
  test("2/3")
  test("2+3-4")
  test("2*3/4")
  test("2+3*4")
  test("2-3/4")
  test("2+3*4-5/10")
  test("0.5+0.1/2.5-1.2")
  test("0.5+0.1/25-12*0.4")
  test("(12-3)*5")
  test("((3-1)/4+2)*5")
  test("(6-2)*2+(8-5)/4")
  test("2+(-5)")
  test("2*(-5)")
  test("3*(2-6)+(1-4)/6")

  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  tokens = evaluateParentheses(tokens)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)

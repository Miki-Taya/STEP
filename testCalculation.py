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


def calculationTimesDivide(tokens):
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


def calculationPlusMinus(tokens):
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


def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  tokens = calculationTimesDivide(tokens)
  answer = calculationPlusMinus(tokens)
  return answer


def parenthesesEvaluate(tokens):        #defeat parentheses.
  index = 0
  parCounter = 0
  leftParIndex = 0
  rightParIndex = 0
  while index < len(tokens):    #get the parCounter and the index of the most right "(".
      if tokens[index]['type'] == 'LEFTPAR':
          leftParIndex = index
          parCounter += 1
          index += 1
      else:
          index += 1
  index = leftParIndex + 4      #for example, the minimum size (3+4) show that ")" is fourth right of "(".
  while index < len(tokens):  #get the index of the most left ")".
      if tokens[index]['type'] == 'RIGHTPAR':
          rightParIndex = index
          break
      else:
          index += 1
  if parCounter == 0:       #until becoming parCOunter==0, repeat parenthesesEvaluate and defeat parentheses.
      print("tokens =",tokens)
      return tokens
  else:
      par = tokens[leftParIndex + 1 : rightParIndex]
      del tokens[leftParIndex : rightParIndex + 1]
      tokens.insert(leftParIndex , {'type':'NUMBER','number':evaluate(par)})    #defeat one parentheses.
      parenthesesEvaluate(tokens)


def test(line):
  tokens = tokenize(line)
  tokens = parenthesesEvaluate(tokens)
  print("after defeating parentheses, tokens =",tokens)
  actualAnswer = evaluate(tokens)
  print(actualAnswer)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  '''
  test("1+2")
  test("1.0+2.1-3")
  test("3*4")
  test("9/3")
  test("1.2*0.3*2")
  test("1.2/3")
  test("12*3+5")
  test("12/3-5")
  test("(12+3)*5")
  test("(12-3)/5")
  test("(1.2-3)*5")
  test("(1.2+3)/5
  test("12+(4+5)*0.1")
  test("2*(1+1)+2/(1+1)")
  test("10*(3+2)/0.5-10*(7-2)")
  '''
  test("2*(((1+3)*2+2)*2+1)")
  test("1+2*2")
  test("2*((2+6)*5+2)")


  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  tokens = parenthesesEvaluate(tokens)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)

from random import uniform,randint
from math import e
from decimal import Decimal,getcontext
from time import time
getcontext().prec = 50

def clear():
  print("\n"*50)

def createSynapses(inputSize,outputSize):
  return([[uniform(-1,1) for column in range(outputSize)] for row in range(inputSize)])

def sigmoidFunction(x,deriv=False):
  if deriv:
    return multiplyValues(x,(subtractValues(1,x)))
  return divideValues(1,addValues(1,powerValues(e,subtractValues(0,x))))

def dotMatrices(aValue,bValue,dropOut=0):
  return [[0 if randint(1,100) <= dropOut else sum([Decimal(aValue[row][i])*Decimal(bValue[i][column]) for i in range(len(bValue))]) for column in range(len(bValue[0]))] for row in range(len(aValue))]

def multiplyValues(aValue,bValue):
  if isinstance(aValue,list) and isinstance(bValue,list):
    return [[aValue[row][column]*bValue[row][column] for column in range(len(aValue[0]))] for row in range(len(aValue))]
  elif isinstance(aValue,list):
    return [[aValue[row][column]*bValue for column in range(len(aValue[0]))] for row in range(len(aValue))]
  elif isinstance(bValue,list):
    return [[aValue*bValue[row][column] for column in range(len(bValue[0]))] for row in range(len(bValue))]
  else:
    return aValue*bValue

def subtractValues(aValue,bValue):
  if isinstance(aValue,list) and isinstance(bValue,list):
    return [[Decimal(aValue[row][column])-bValue[row][column] for column in range(len(aValue[0]))]for row in range(len(aValue))]
  elif isinstance(aValue,list):
    return [[aValue[row][column]-bValue for column in range(len(aValue[0]))] for row in range(len(aValue))]
  elif isinstance(bValue,list):
    return [[aValue-bValue[row][column] for column in range(len(bValue[0]))] for row in range(len(bValue))]
  else:
    return aValue-bValue

def addValues(aValue,bValue):
  if isinstance(aValue,list) and isinstance(bValue,list):
    return [[Decimal(aValue[row][column])+Decimal(bValue[row][column]) for column in range(len(aValue[0]))]for row in range(len(aValue))]
  elif isinstance(aValue,list):
    return [[aValue[row][column]+bValue for column in range(len(aValue[0]))] for row in range(len(aValue))]
  elif isinstance(bValue,list):
    return [[aValue+bValue[row][column] for column in range(len(bValue[0]))] for row in range(len(bValue))]
  else:
    return aValue+bValue

def divideValues(aValue,bValue):
  if isinstance(aValue,list):
    return [[aValue[row][column]/bValue for column in range(len(aValue[0]))] for row in range(len(aValue))]
  elif isinstance(bValue,list):
    return [[aValue/bValue[row][column] for column in range(len(bValue[0]))] for row in range(len(bValue))]
  else:
    return aValue/bValue
  
def powerValues(aValue,bValue):
  if isinstance(aValue,list):
    return [[aValue[row][column]**bValue for column in range(len(aValue[0]))] for row in range(len(aValue))]
  elif isinstance(bValue,list):
    return [[Decimal(aValue)**Decimal(bValue[row][column]) for column in range(len(bValue[0]))] for row in range(len(bValue))]
  else:
    return aValue**bValue

def transformMatrix(aMatrix):
  return [[aMatrix[row][column] for row in range(len(aMatrix))] for column in range(len(aMatrix[0]))]

def replaceZero(aMatrix):
  return [[Decimal(aMatrix[row][column]) if aMatrix[row][column] != 0 else Decimal(0.1) for column in range(len(aMatrix[0]))] for row in range(len(aMatrix))]

def absoluteValues(aMatrix):
  return [[abs(aMatrix[row][column]) for column in range(len(aMatrix[0]))] for row in range(len(aMatrix))]

def averageValue(aMatrix):
  listy = [aMatrix[row][column] for column in range(len(aMatrix[0])) for row in range(len(aMatrix))]
  return sum(listy)/len(listy)

def maxValue(aMatrix):
  listy = [aMatrix[row][column] for column in range(len(aMatrix[0])) for row in range(len(aMatrix))]
  return max(listy)

def minValue(aMatrix):
  listy = [aMatrix[row][column] for column in range(len(aMatrix[0])) for row in range(len(aMatrix))]
  return min(listy)

########################## Change this ############################

# 1 - len / 25, 2 - wid / 5

inputData = [[0,0,0],
            [1,0,1],
            [0,1,1],
            [0,1,0],
            [1,1,1],
            [0,1,0]]

outputData =  [[0,0,1],
              [1,1,0],
              [1,0,0],
              [0,1,1],
              [0,0,0],
              [0,1,1]]

synapseSizes = [[3,8],[8,3]]

trainingTime = 10

dropoutPercent = 20

def processData(string):
  return replaceZero([[float(i) for i in string.split()]])

def outputAnswer(listy):
  print(listy)

def wrongDetected():
  if input() == "False":
    return [0]
  else:
    return [1]

######################################################################################

def train():
  global synapseList
  repeatUntil = time() + trainingTime
  lastSecond = int(((repeatUntil+1)-time())//1)
  loops = 0
  bestLoss = 1
  while time() < repeatUntil:
    for k in range(len(inputData)):
      if loops % 10 == 0:
        tempList = []
        tempList.append(inputData)
        for i in range(len(synapseSizes)):
          tempList.append(sigmoidFunction(dotMatrices(tempList[i],synapseList[i])))
        if averageValue(absoluteValues(subtractValues(outputData,tempList[-1]))) <= bestLoss:
          synapseBest = synapseList
          bestLoop = loops
          bestLoss = averageValue(absoluteValues(subtractValues(outputData,tempList[-1])))
      layerList = []
      layerList.append([inputData[k]]) # Sets the first layer to the input data
      for i in range(len(synapseSizes)):
        layerList.append(sigmoidFunction(dotMatrices(layerList[i],synapseList[i],dropoutPercent if i != len(synapseSizes)-1 else 0)))
      deltaList = []
      deltaList.append(multiplyValues(subtractValues([outputData[k]],layerList[-1]),sigmoidFunction(layerList[-1],True)))
      for i in range(len(synapseSizes)-1):
        deltaList.append(multiplyValues(dotMatrices(deltaList[i],transformMatrix(synapseList[-(1+i)])),sigmoidFunction(layerList[-(2+i)],True)))
      for i in range(len(synapseSizes)):
        synapseList[-(1+i)] = addValues(synapseList[-(1+i)],dotMatrices(transformMatrix(layerList[-(2+i)]),deltaList[i]))
      loops += 1/len(inputData)
      if 0 <= (repeatUntil-time())//1 < lastSecond:
        clear()
        lastMinute = int((repeatUntil-time())//60)
        lastSecond = int((repeatUntil-time())//1)
        print(lastMinute, lastSecond%60)
  tempList = []
  tempList.append(inputData)
  for i in range(len(synapseSizes)):
    tempList.append(sigmoidFunction(dotMatrices(tempList[i],synapseList[i])))
  if averageValue(absoluteValues(subtractValues(outputData,tempList[-1]))) <= bestLoss:
    bestLoop = loops
    synapseBest = synapseList
    bestLoss = averageValue(absoluteValues(subtractValues(outputData,tempList[-1])))
  clear()
  print("The network trained " + str(int(round(loops))) + " times.")
  print("It achieved an accuracy of "+str(100-bestLoss*100)+"%")
  print("It peaked at loop " + str(round(bestLoop))+".")

def run():
  global synapseList
  global inputData
  global outputData
  inputData = replaceZero(inputData)
  outputData = [[float(i) for i in outputData[x]] for x in range(len(outputData))]
  synapseList = []
  synapseBest = []
  for item in synapseSizes:
    synapseList.append(createSynapses(item[0],item[1]))
  train()
  tempInput = input()
  while tempInput != "wrong":
    testValues = processData(tempInput)
    layerList = []
    layerList.append(testValues) # Sets the first layer to the input data
    for i in range(len(synapseSizes)):
      layerList.append(sigmoidFunction(dotMatrices(layerList[i],synapseList[i])))
    outputAnswer(layerList[-1][0])
    tempInput = input()
  correctAnswer = wrongDetected()
  inputData.append(testValues[0])
  outputData.append(correctAnswer)
  run()

  
run()
import numpy as np

def interpretData(fileName,numData,numElements,inputElements,outputElements,onlyComplete = True,elementBit=4):
  global binaryRanges
  global inputElementList
  global outputElementList
  inputElementList=inputElements
  outputElementList=outputElements
  binaryRanges = dict()
  completeData = open(fileName).read().replace("\n"," ").split()
  excludeData = []
  if onlyComplete:
    for dataID in range(numData):
      for element in inputElements + outputElements:
        if float(completeData[(numElements*dataID)+element-1]) < 0:
          excludeData.append(dataID)
          break
  inputData = []
  outputData = []
  rangeDict = dict()
  for dataID in range(numData):
    if not dataID in excludeData:
      inputList = []
      outputList = []
      for inputElement in inputElements:
        inputList.append(float(completeData[(numElements*dataID)+inputElement-1]))
        rangeDict[inputElement] = rangeDict.get(inputElement,[999999999,-9])
        if float(completeData[(numElements*dataID)+inputElement-1]) < rangeDict[inputElement][0]:
          rangeDict[inputElement][0] = float(completeData[(numElements*dataID)+inputElement-1])
        if float(completeData[(numElements*dataID)+inputElement-1]) > rangeDict[inputElement][1]:
          rangeDict[inputElement][1] = float(completeData[(numElements*dataID)+inputElement-1])
      for outputElement in outputElements:
        outputList.append(float(completeData[(numElements*dataID)+outputElement-1]))
        rangeDict[outputElement] = rangeDict.get(outputElement,[999999999,-9])
        if float(completeData[(numElements*dataID)+outputElement-1]) < rangeDict[outputElement][0]:
          rangeDict[outputElement][0] = float(completeData[(numElements*dataID)+outputElement-1])
        if float(completeData[(numElements*dataID)+outputElement-1]) > rangeDict[outputElement][1]:
          rangeDict[outputElement][1] = float(completeData[(numElements*dataID)+outputElement-1])
      inputData.append(inputList)
      outputData.append(outputList)
  for key in rangeDict:
    minimum,maximum = rangeDict[key]
    dataRange = round(maximum-minimum)
    definition = []
    if dataRange < elementBit:
      for i in range(dataRange+1):
        if minimum+i!=0:
          definition.append(minimum+i)
    else:
      increment = (dataRange/elementBit)//1
      for i in range(elementBit+1):
        definition.append(minimum+(i*increment))
    binaryRanges[key] = definition
  processedInputData = []
  processedOutputData = []
  for listValues in inputData:
    processedInputData.append(convertData(listValues))
  for listValues in outputData:
    processedOutputData.append(convertData(listValues,inputData=False))
  return processedInputData, processedOutputData

def convertData(listValues,inputData=True):
  if inputData:
    valueKeys = inputElementList
  else:
    valueKeys = outputElementList
  returnList = []
  for i in range(len(listValues)):
    currentNum = listValues[i]
    for j in range(len(binaryRanges[valueKeys[i]])-1):
      if currentNum >= binaryRanges[valueKeys[i]][j] and currentNum < binaryRanges[valueKeys[i]][j+1]:
        returnList.append(1)
      else:
        returnList.append(0)
    if currentNum >= binaryRanges[valueKeys[i]][-1]:
        returnList.append(1)
    else:
      returnList.append(0)
  return(returnList)

inputData, outputData = interpretData("completeData.txt",1541,90,[3,4,9,17,32,33],[58])
print(inputData)
print(outputData)
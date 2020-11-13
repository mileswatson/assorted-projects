from time import time
from random import randint

def linearSearch(sortList,findValue,timeIt=False):
    if timeIt:
        startTime = time()
        for i in range(len(sortList)):
            if sortList[i] == findValue:
                return time()-startTime
        return None
    else:
        dictionary = {"comparison":0,"integer calculation":0}
        for i in range(len(sortList)):
            dictionary["comparison"] += 1
            dictionary["integer calculation"] += 1
            dictionary["comparison"] += 1
            if sortList[i] == findValue:
                return dictionary
        return None



def binarySearch(listy,val):
  minimum = 0
  maximum = len(listy)
  while minimum <= maximum:
      testNum = (minimum + maximum)//2
      if listy[testNum] == val:
          return testNum
      elif listy[testNum] > val:
          maximum = testNum - 1
      elif listy[testNum] < val:
          minimum = testNum + 1
  return None

def bubbleSort(array):
    limit = len(array)-1
    while limit > 0:
        swap = False
        for i in range(limit):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
                swap = True
        if not swap:
            break
        limit -= 1
    return array

def insertionSort(array):
    for splitPoint in range(1,len(array)):
        currentVal = array[splitPoint]
        i = splitPoint
        while i > 0 and array[i-1]>currentVal:
            array[i] = array[i-1]
            i-=1
        array[i] = currentVal
    return array


def mergeSort(array):
    if len(array) > 1:
        divide = len(array)//2
        left = mergeSort(array[:divide])
        right = mergeSort(array[divide:])

        leftCount = 0
        rightCount = 0
        insertLocation = -1
        
        while leftCount < len(left) and rightCount < len(right):
            insertLocation += 1
            if left[leftCount] < right[rightCount]:
                array[insertLocation] = left[leftCount]
                leftCount += 1
            else:
                array[insertLocation] = right[rightCount]
                rightCount += 1
        
        while leftCount < len(left):
            insertLocation += 1
            array[insertLocation] = left[leftCount]
            leftCount += 1

        while rightCount < len(right):
            insertLocation += 1
            array[insertLocation] = right[rightCount]
            rightCount += 1
    return array

def insertionSortBS(array):
  for splitPoint in range(1,len(array)):
    currentVal = array[splitPoint]
    minimum = 0
    maximum = splitPoint-1
    reduced = None
    while minimum <= maximum:
        testNum = (minimum + maximum)//2
        if array[testNum] == currentVal:
            break
        elif array[testNum] > currentVal:
            maximum = testNum - 1
            reduced = True
        elif array[testNum] < currentVal:
            minimum = testNum + 1
            reduced = False
    if minimum <= maximum:
      if reduced == True:
        testNum = minimum
      else:
        testNum = maximum
    array[testNum+1:splitPoint+1] = array[testNum:splitPoint]
    array[testNum] = currentVal
  return array

def unsortedBinarySort(array,val):
  for splitPoint in range(1,len(array)):
    currentVal = array[splitPoint]
    minimum = 0
    maximum = splitPoint-1
    reduced = None
    while minimum <= maximum:
        testNum = (minimum + maximum)//2
        if array[testNum] == currentVal:
            break
        elif array[testNum] > currentVal:
            maximum = testNum - 1
            reduced = True
        elif array[testNum] < currentVal:
            minimum = testNum + 1
            reduced = False
    if minimum <= maximum:
      if reduced == True:
        testNum = minimum
      else:
        testNum = maximum
    array[testNum+1:splitPoint+1] = array[testNum:splitPoint]
    array[testNum] = currentVal
  minimum = 0
  maximum = len(array)
  while minimum <= maximum:
      testNum = (minimum + maximum)//2
      if array[testNum] == val:
          return testNum
      elif array[testNum] > val:
          maximum = testNum - 1
      elif array[testNum] < val:
          minimum = testNum + 1
  return None

epochs = 3
lengths = 6000

arrays = [[randint(0,lengths) for j in range(lengths)] for i in range(epochs)]
print("Arrays generated")
startTime = time()
for array in arrays:
  insertionSort(array)
  print("done one")
endTime = time()
print("regular insertion:",(endTime-startTime)/epochs)

startTime = time()
for array in arrays:
  insertionSortBS(array)
endTime = time()
print("BS insertion:",(endTime-startTime)/epochs)





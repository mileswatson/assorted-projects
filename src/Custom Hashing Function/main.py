from time import time
def hash256(string,salt="abcdefghijklmnopqrstuvwxyz"):
  outputBitNum = 256
  key1 = 2
  key2 = ((2**outputBitNum)-1)
  string = (" "*16) + salt + string
  bigList = []
  for i in range(len(string)):
    tempString = "{0:b}".format((ord(string[i])**key1)%255)
    for bit in tempString:
      bigList.append(str(bit))
  bigList += ["0"] * (outputBitNum - (len(bigList) % outputBitNum))
  lastNum = ["0"]*(outputBitNum-1) + ["1"]
  iterations = len(bigList)//outputBitNum
  for i in range(iterations):
    firstNum = int("".join(bigList[i*outputBitNum:(i+1)*outputBitNum]),2) * (int("".join(lastNum),2)**2)
    lastNum = list("{0:b}".format((firstNum**key1)%key2))
    lastNum += ["0"] * (outputBitNum - (len(lastNum) % outputBitNum))
    lastNum = lastNum[:outputBitNum]
    #if (i+1) % 1000 == 0:
    #  print(i+1,"/",iterations)
  return(str(hex(int("".join(lastNum),2))[2:]))

data = open("file.txt","r")
data = data.read()
print("File read, beginning hash.")
#startTime = time()
data = hash256("a")
#finishTime = time() - startTime
print(data)
#print(finishTime)
print(hash256("j"))
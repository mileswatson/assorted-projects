from random import randint
from datetime import datetime

class crypter(object):
  
  @staticmethod
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
    return(str(hex(int("".join(lastNum),2))[2:]))
  
  @staticmethod
  def getPrime(start_num):
    start_num -= 2
    prime_num = 5
    if start_num % 2 == 0:
      start_num = start_num + 1
    found = False
    test_num = start_num
    while found == False:
      test_num += 2
      limit = round(test_num ** 0.5)
      test_for = 1
      prime = True
      while test_for <= limit:
        test_for += 2
        if test_num % test_for == 0:
          prime = False
          test_for = limit + 1
      if prime == True:
        prime_num = test_num
        found = True
    return(prime_num)
  
  @staticmethod
  def getKeys():
    area_specific_value = randint(111,999)
    p = crypter.getPrime(area_specific_value)
    area_specific_value = randint(111,999)
    q = crypter.getPrime(area_specific_value)
    n = p * q
    totient_n = (p-1) * (q-1)
    area_specific_value = randint(111,totient_n)
    e = crypter.getPrime(area_specific_value)
    loop = True
    d = 1
    while loop == True:
      x = (e * d - 1) % totient_n
      if x == 0:
        loop = False
      else:
        d += 1
    return [max(e,d),n,min(e,d)]
  
  @staticmethod
  def encrypt(string,key,sharedKey):
    numbers = []
    string = list(string)
    length = len(string)
    for i in range (0,length):
      numbers.append(hex((((int(ord(string[i]))+(i + 1)) ** key) % sharedKey)).replace("0x",""))
    return " ".join(numbers)
  
  @staticmethod
  def decrypt(string,key,identifier):
    numbers = []
    string = string.split()
    length = len(string)
    for i in range (0,length):
      numbers.append(chr(int(((int(string[i], 16) ** key) % identifier) - (i+1))))
    return "".join(numbers)

class user(object):
  numUsers = 0
  def __init__(self,name,password,privateKey,sharedKey,publicKey,verification="unverified"):
    self.name = name
    self.verification = verification
    if privateKey == None:
      privateKey,sharedKey,publicKey = crypter.getKeys()
      print("IMPORTANT: YOUR PRIVATE KEY IS "+str(privateKey)+". REMEMBER THIS NUMBER, OR YOU WILL NO LONGER BE ABLE TO SIGN DOCUMENTS!")
      input("PRESS ENTER TO CONTINUE")
      print("\n"*50)
      self.password = crypter.hash256(password,salt=self.name)
      self.privateKey = crypter.hash256(str(privateKey),salt=self.name)
    else:
      self.password = password
      self.privateKey = privateKey
    self.sharedKey = int(sharedKey)
    self.publicKey = int(publicKey)
  
  def verify(self):
    self.verification = "verified"
  
  def unverify(self):
    self.verification = "unverified"
  
  @staticmethod
  def sign(username,password,privateKey,fileName,userDict):
    if username in userDict:
      currentUser = userDict[username]
      if crypter.hash256(password,salt=currentUser.name) == currentUser.password and crypter.hash256(privateKey,salt=currentUser.name) == currentUser.privateKey:
        file = open(fileName,"r")
        hashedFile = crypter.hash256(file.read())
        file.close()
        date = input("What date should this be valid until?")
        file = open(fileName,"a")
        appendage = crypter.encrypt("//".join([date,hashedFile]),int(privateKey),int(currentUser.sharedKey))
        appendage = "//Authenticate this file with SignMyFile//"+username+"//"+appendage
        file.write(appendage)
        file.close()
        return True
    return False
  
  @staticmethod
  def authenticate(file,userDict):
    file = open(file,"r")
    completeData = file.read().split("//")
    data = completeData[-3:]
    file.close()
    if data[0] == "Authenticate this file with SignMyFile":
      if data[1] in userDict:
        signedBy = userDict[data[1]]
        decryptedData = crypter.decrypt(data[2],signedBy.publicKey,signedBy.sharedKey).split("//")
        day,month,year = [int(i) for i in decryptedData[0].split()]
        expires = datetime(year,month,day)
        if datetime.now()<expires:
          whatHash = "//".join(completeData[:-3]) if len(completeData)>4 else completeData[0]
          if crypter.hash256(whatHash) == decryptedData[1]:
            return "This file was signed by " + data[1] + " (" + signedBy.verification + " "+signedBy.name+")."
        return "The signiture is invalid."
      return "The signiture is not in your user database."
    return "This file has not been signed using SignMyFile."
  
  @staticmethod
  def getUsers():
    returnDict = dict()
    file = open("saveData.txt","r")
    data = file.read()
    file.close()
    if data == "":
      return returnDict
    else:
      data = [i.split("//") for i in data.split("\n")][:-1]
      for item in data:
        returnDict[item[0]] = user(item[1],item[2],item[3],int(item[4]),int(item[5]),verification=item[6])
        user.numUsers += 1
      return returnDict
  
  @staticmethod
  def saveUsers(userDict):
    file = open("saveData.txt","w")
    for item in userDict:
      aUser = userDict[item]
      string = "//".join([item,aUser.name,aUser.password,aUser.privateKey,str(aUser.sharedKey),str(aUser.publicKey),aUser.verification])+"\n"
      file.write(string)
    file.close()
    
userDict = user.getUsers()
while True:
  x = input("What would you like to do?").lower()
  if x == "sign":
    user.sign(input("Enter your username:"),input("Enter your password:"),input("Enter your private key:"),input("Enter the file name:"),userDict)
  elif x == "authenticate":
    print(user.authenticate(input("Enter the filename:"),userDict))
  elif x == "create":
    whichUsername = input("Enter your username:")
    if not whichUsername in userDict:
      name = input("Enter name:")
      password = input("Enter your password:")
      if password == input("Re-enter your password:"):
        userDict[whichUsername] = user(name,password,None,None,None)
  elif x == "quit":
    break
  else:
    print("That is not a valid input.")
  user.saveUsers(userDict)





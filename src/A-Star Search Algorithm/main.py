from math import sqrt


class storeNode:
  def __init__(self,pos,connections=[]):
    self.pos = pos
    self.connections = connections
    self.name = str(pos[0]) + chr(0) + str(pos[1])
    
class activeNode:
  def __init__(self,copyNode):
    self.pos = copyNode.pos
    self.connections = copyNode.connections
    if type(copyNode) == activeNode:
      self.fromStart = copyNode.fromStart
      self.toEnd = copyNode.toEnd
    else:
      self.fromStart = -1
      self.toEnd = -1
    self.name = str(self.pos[0]) + chr(0) + str(self.pos[1])
  
  def setToEnd(self,pos):
    self.toEnd = sqrt(((self.pos[0]-pos[0])**2)+((self.pos[1]-pos[1])**2)) / (sum([value for key, value in self.connections]) / len(self.connections))

class nodeMap:
  def __init__(self):
    self.nodes = []
  
  def nodeFile(self,filename):
    file = open(filename,"r")
    data = file.read()
    file.close()
    for nodeData in data.split("\n"):
      nodeData = nodeData.split("=")
      pos = nodeData[0].split(",")
      pos = (int(pos[0]),int(pos[1]))
      connections = []
      for connection in nodeData[1].split(";"):
        if connection != "":
          conPos, speed = connection.split(":")
          conPos = conPos.split(",")
          conPos = (int(conPos[0]),int(conPos[1]))
          connections.append(((conPos),int(speed)))
      self.addNode(storeNode(pos,connections))
      

  def addNode(self,node):
    if len(self.nodes) == 0:
      self.nodes.append(node)
    else:
      minimum = 0
      maximum = len(self.nodes)
      while minimum < maximum:
          split = (minimum + maximum) // 2
          if self.nodes[split].name == node.name:
              break
          elif self.nodes[split].name < node.name:
              minimum = split + 1
          else:
              maximum = split
      self.nodes.insert(split + 1, node)
  
  def getNode(self,pos):
    name = str(pos[0]) + chr(0) + str(pos[1])
    minimum = 0
    maximum = len(self.nodes)
    while minimum < maximum:
        split = (minimum + maximum) // 2
        if self.nodes[split].name == name:
            a = activeNode(self.nodes[split])
            #if delete:
              #del self.nodes[split]
            return a
        elif self.nodes[split].name < name:
            minimum = split + 1
        else:
            maximum = split
    return None
  
  def removeNode(self,pos):
    name = str(pos[0]) + chr(0) + str(pos[1])
    minimum = 0
    maximum = len(self.nodes)
    while minimum < maximum:
        split = (minimum + maximum) // 2
        if self.nodes[split].name == name:
            del self.nodes[split]
            return True
        elif self.nodes[split].name < name:
            minimum = split + 1
        else:
            maximum = split
    return False
  
  def getLowest(self):
    minimum = -1
    location = -1
    for i in range(len(self.nodes)):
      value = self.nodes[i].fromStart + self.nodes[i].toEnd
      if value > minimum and value > 0:
        minimum = self.nodes[i].value
        location = i
    return self.nodes.pop(location)
  
  def getNearest(self,pos):
    minimum = -1
    first = True
    location = -1
    for i in range(len(self.nodes)):
      if sqrt((abs(self.nodes[i].pos[0]-pos[0])**2)+(abs(self.nodes[i].pos[1]-pos[1])**2)) < minimum or first:
        minimum = sqrt((abs(self.nodes[i].pos[0]-pos[0])**2)+(abs(self.nodes[i].pos[1]-pos[1])**2))
        location = i
        first = False
    return activeNode(self.nodes[location])

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

class aStar:
  
  def __init__(self,nmp,pos=(0,0)):
    self.nmp = nmp
    x = self.nmp.getNearest(pos)
    self.path = [x]
  
  def addPoint(self,pos):
    activeMap = nodeMap()
    passiveMap = nodeMap()
    x = self.path[-1]
    x.setToEnd(0)
    x.fromStart = 0
    searching, evaluated = True, True
    destination = self.nmp.getNearest(pos)
    while evaluated and searching:
      evaluated = False
      currentNode = activeMap.getLowest()
      for connection, speed in currentNode.connections:
        if connection == destination.pos:
          break
        x = activeMap.getNode(connection)
        tmp = 0
        if type(x) != activeNode:
          x = passiveMap.getNode(connection)
          tmp = 1
          if type(x) != activeNode:
            x = self.nmp.getNode(connection)
            tmp = 2
            if type(x) != activeNode:
              continue
        value = sqrt(((currentNode.pos[0]-x.pos[0])**2)+((currentNode.pos[1]-x[1])**2)) / speed
        if x.fromStart < 0 or x.fromStart > value:
          x.fromStart = value
          if tmp == 1:
            passiveMap.removeNode(connection)
            activeMap.addNode(x)
        activeMap.removeNode(currentNode.pos)
        passiveMap.addNode(currentNode)
        
        
      
    


nmp = nodeMap()
nmp.nodeFile("nodeData.txt")
x = aStar(nmp,(0,1))
x.addPoint((2,2))












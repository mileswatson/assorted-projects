from time import time

startTime = time()

class node:
    def __init__(self):
        self.connections = dict()
        self.distance = 0
    def add(self,name, distance):
        self.connections[name] = distance

nodes = dict()
opn = dict()
closed = dict()

townNames = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
'v','w','x','y','z')

connections = [['a','b',1],['a','h',2],['a','u',3],['b','c',1],['b','o',2],['c','j',4],['c','p',3],['d','k',2],['d','l',1],['d','x',1],['e','f',4],['e','r',2],['f','m',3],['f','s',2],['g','z',2],['h','b',1],['i','c',3],['i','j',2],['j','d',5],['k','e',2],['l','f',2],['l','m',2],['l','y',3],['m','g',1],['n','h',5],['n','o',2],['o','i',1],['p','q',1],['p','w',2],['q','k',2],['q','r',1],['r','l',2],['s','t',4],['t','z',1],['u','p',2],['v','p',7],['w','q',3],['x','s',1],['y','s',2]]

start = 'a'
finish = 'z'

for i in townNames:
    nodes[i] = node()

for i in connections:
    nodes[i[0]].connections[i[1]] = i[2]
    nodes[i[1]].connections[i[0]] = i[2]

opn[start] = nodes[start]

while len(opn) > 0:
    ordered = sorted(opn, key = lambda name: opn[name].distance)
    current = opn.pop(ordered[0])
    for name in current.connections:
        if name in opn:
            if opn[name].distance > current.distance + current.connections[name]:
                opn[name].distance = current.distance + current.connections[name]
        elif name in closed:
            if closed[name].distance > current.distance + current.connections[name]:
                closed[name].distance = current.distance + current.connections[name]
                opn[name] = closed.pop(name)
        else:
            nodes[name].distance = current.distance + current.connections[name]
            opn[name] = nodes[name]
    closed[ordered[0]] = current
#for name in closed:
    #print(name + " = " + str(closed[name].distance))

solution = ""
currentName = finish
while currentName != start:
    solution += currentName
    currentNode = closed.pop(currentName)
    currentName = min(currentNode.connections, key = lambda x: nodes[x].distance)
solution = start + solution[::-1]
print(time()-startTime)
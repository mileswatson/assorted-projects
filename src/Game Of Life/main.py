from random import randint
from time import sleep
import os


class cell:
  
  def __init__(self,state="None"):
    if state == "None":
      self.alive = False if randint(0,1) == 0 else True
    else:
      self.alive = state
  
class game:
  
  def __init__(self,dimensions,fps):
    self.board = [[cell(state=i) for i in array] for array in self.seed(dimensions)]
    self.dimensions = (len(self.board),len(self.board[0]))
    self.wait = 1/fps
    self.run()
  
  def seed(self,dimensions):
    return [[True if randint(0,2) == 0 else False for j in range(dimensions[0])] for i in range(dimensions[1])]
  
  def run(self):
    while True:
      self.clear()
      aBoard = [[cell(aCell.alive) for aCell in array] for array in self.board]
      for xa in range(self.dimensions[0]):
        for ya in range(self.dimensions[1]):
          numNeighbours = 0
          currentCell = self.board[xa][ya]
          for xb in range(xa-1,xa+2):
            for yb in range(ya-1,ya+2):
              if 0 <= xb < self.dimensions[0] and 0 <= yb < self.dimensions[1]:
                neighbourCell = self.board[xb][yb]
                if neighbourCell.alive and [xa,ya] != [xb,yb]:
                  numNeighbours += 1
          if currentCell.alive:
            if numNeighbours < 2 or numNeighbours > 3:
              aBoard[xa][ya] = cell(state=False)
            else:
              aBoard[xa][ya] = cell(state=True)
          elif numNeighbours == 3:
            aBoard[xa][ya] = cell(state=True)
          else:
            aBoard[xa][ya] = cell(state=False)
          print()
      self.board = aBoard
      for array in self.board:
        print("".join(["@" if aCell.alive else " " for aCell in array]))
      sleep(self.wait)
  
  def clear(self):
    #print("\n"*50)
    print("\033c")

game((40,25),2)








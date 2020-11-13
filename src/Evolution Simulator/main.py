import numpy as np

from galapagos import Island, save, load
import galapagos.finches as finches
import galapagos.activations as activations

from random import randint, uniform
from time import sleep, time

class SnakeGame(Island):
    
    SIZE = 16
    DIRECTIONS = {
        "UP":np.asarray([1,0,0,0]),
        "RIGHT":np.asarray([0,1,0,0]),
        "DOWN":np.asarray([0,0,1,0]),
        "LEFT":np.asarray([0,0,0,1])
    }
    ITERATIONS = 5
    LIMIT = 100

    def test(self, finch, show=False):
        self.score = 0
        for i in range(SnakeGame.ITERATIONS if not show else 1):
            self.setup_game()
            finch.forget()
            i = 0
            while self.alive and i < SnakeGame.LIMIT:
                senses = self.get_input_array()
                reaction = list(finch.react(senses)[0])
                current_heading_index = (["UP", "RIGHT", "DOWN", "LEFT"].index(self.heading)+2)%4
                reaction[current_heading_index] = 0
                self.heading = ["UP", "RIGHT", "DOWN", "LEFT"][reaction.index(max(reaction))]
                self.move_snake()
                if show:
                    #print(senses)
                    self.print_board()
                    sleep(0.1)
                i += 1
                self.score += 1
        finch.forget()
        if not show:
            finch.score(self.score/SnakeGame.ITERATIONS)
    
    def setup_game(self):
        self.alive = True
        self.heading = "UP"
        self.grid = np.asarray([[0 for i in range(SnakeGame.SIZE)] for i in range(SnakeGame.SIZE)])
        midpoint = SnakeGame.SIZE//2
        self.snake = [(midpoint, midpoint),(midpoint+1, midpoint),(midpoint+2, midpoint)]
        for i in range(len(self.snake)):
            pos = self.snake[i]
            if i == 0:
                self.grid[pos[0]][pos[1]] = 2
            else:
                self.grid[pos[0]][pos[1]] = 1
        self.new_fruit()
        
        
    def move_snake(self):
        tail = self.snake[-1]
        self.set_pos(tail, 0)
        head = self.snake[0]
        self.set_pos(head, 1)
        if self.heading == "UP":
            head = (head[0]-1, head[1])
        elif self.heading == "RIGHT":
            head = (head[0], head[1]+1)
        elif self.heading == "DOWN":
            head = (head[0]+1, head[1])
        elif self.heading == "LEFT":
            head = (head[0], head[1]-1)
        self.snake.insert(0, head)
        if min(head) == -1 or max(head) == SnakeGame.SIZE:
            self.alive = False
            return
        status = self.get_pos(head)
        if status == 1:
            self.alive = False
        if status == 3:
            self.new_fruit()
            self.score += 100
        else:
            self.snake = self.snake[:-1]
        self.set_pos(head, 2)
        
    
    def new_fruit(self):
        self.fruit = (randint(0, SnakeGame.SIZE-1),randint(0, SnakeGame.SIZE-1))
        while self.grid[self.fruit[0]][self.fruit[1]] != 0:
            self.fruit = (randint(0, SnakeGame.SIZE-1),randint(0, SnakeGame.SIZE-1))
        self.grid[self.fruit[0]][self.fruit[1]] = 3
    
    def get_input_array(self):
        head = self.snake[0]
        
        up = [head[0], SnakeGame.SIZE, SnakeGame.SIZE]
        for i in range(head[0]):
            stat = self.get_pos((head[0]-i-1, head[1]))
            if stat == 1 and up[1] == SnakeGame.SIZE:
                up[1] = i
            if stat == 3 and up[2] == SnakeGame.SIZE:
                up[2] = i
        
        down = [SnakeGame.SIZE-head[0]-1, SnakeGame.SIZE, SnakeGame.SIZE]
        for i in range(SnakeGame.SIZE-head[0]-1):
            stat = self.get_pos((head[0]+i+1, head[1]))
            if stat == 1 and down[1] == SnakeGame.SIZE:
                down[1] = i
            if stat == 3 and down[2] == SnakeGame.SIZE:
                down[2] = i
        
        left = [head[1], SnakeGame.SIZE, SnakeGame.SIZE]
        for i in range(head[1]):
            stat = self.get_pos((head[0], head[1]-i-1))
            if stat == 1 and left[1] == SnakeGame.SIZE:
                left[1] = i
            if stat == 3 and left[2] == SnakeGame.SIZE:
                left[2] = i
        
        right = [SnakeGame.SIZE-head[1]-1, SnakeGame.SIZE, SnakeGame.SIZE]
        for i in range(SnakeGame.SIZE-head[1]-1):
            stat = self.get_pos((head[0], head[1]+i+1))
            if stat == 1 and right[1] == SnakeGame.SIZE:
                right[1] = i
            if stat == 3 and right[2] == SnakeGame.SIZE:
                right[2] = i
        
        return (SnakeGame.SIZE-np.atleast_2d(np.asarray(up+right+down+left)))/SnakeGame.SIZE
            
        #return np.atleast_2d(np.append(self.grid.flatten(), SnakeGame.DIRECTIONS[self.heading]))
    
    def print_board(self):
        s = "\n"*50
        s += "Score: " + str(self.score) + "\n"
        s += "# " + "- " * (self.SIZE) + "#\n"
        for row in self.grid:
            s += "| "+" ".join([" #@$"[i] for i in row]) + " |\n"
        s += "# " + "- " * (self.SIZE) + "#\n"
        print(s)
    
    def set_pos(self, pos, value):
        self.grid[pos[0]][pos[1]] = value

    def get_pos(self, pos):
        return self.grid[pos[0]][pos[1]]




island = SnakeGame(
    finch_type = finches.NeuralNetwork,
    num_finches = 500,
    args = {
        "shape":(
            12,
            4
        ),
        "activation":activations.sigmoid,
        "mutation":0.2,
        "memory":6
    }
)

island.pressure()
while True:
    user_input = input("Enter command: ")
    if user_input == "TRAIN":
        user_input=input("Enter seconds: ")
        end_time = time()+int(user_input)
        while time() < end_time:
            island.select()
            island.pressure()
            print(island.average(), island.best())
            save(island, "island.pickle")
    elif user_input == "TEST":
        island.test(island.best(),show=True)
    elif user_input == "LIMIT":
        x = int(input("Enter move limit: "))
        SnakeGame.LIMIT = x
    elif user_input == "SAVE":
        x = input("Enter filename: ")
        save(island, x)
    elif user_input == "LOAD":
        x = input("Enter filename: ")
        island = load(x)
    elif user_input == "NEW":
        island = SnakeGame(
            finch_type = finches.NeuralNetwork,
            num_finches = 500,
            args = {
                "shape":(
                    12,
                    4
                ),
                "activation":activations.sigmoid,
                "mutation":0.2,
                "memory":6
            }
        )
    else:
        print("Invalid Command")
    print()

print(island)


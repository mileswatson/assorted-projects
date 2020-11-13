from galapagos.finches import Finch
import copy
import pickle

class Island:

    def __init__(self, finch_type=Finch, num_finches=100, args=None):
        if not args:
            args = dict()
        self.finches = [finch_type(args) for i in range(num_finches)]
    
    def pressure(self):
        for finch in self.finches:
            self.test(finch)
    
    def test(self, finch):
        finch.score(0)
        
    def select(self):
        self.finches.sort(key = lambda finch: finch.fitness, reverse=True)
        self.finches = self.finches[:len(self.finches)//2]
        for i in range(len(self.finches)):
            finch = self.finches[i]
            offspring = copy.deepcopy(finch)
            offspring.mutate()
            self.finches += [offspring]
            finch.mutate()
    
    def average(self):
        return sum([f.fitness for f in self.finches])/len(self.finches)
    
    def best(self):
        return max(self.finches, key = lambda x: x.fitness)
    
    def __str__(self):
        self.finches.sort(key = lambda x: x.fitness)
        return "\n\n".join([str(finch) for finch in self.finches]) + "\n"
    
def save(obj, file_name):
    f = open(file_name, "wb")
    pickle.dump(obj, f)
    f.close()

def load(file_name):
    f = open(file_name, "rb")
    x = pickle.load(f)
    f.close()
    return x
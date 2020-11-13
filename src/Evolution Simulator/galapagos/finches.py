import numpy as np
from random import randint, uniform

import galapagos.activations

class Finch:
    
    defaults = {

    }

    def __init__(self, args):
        self.fitness = 0
    
    def forget(self):
        pass
    
    def score(self, fitness):
        self.fitness = fitness
    
    def react(self, inputs):
        raise NotImplimentedError("'Finch' is a class template, and is not intended to be used as a real class.")
    
    def mutate(self):
        raise NotImplimentedError("'Finch' is a class template, and is not intended to be used as a real class.")
    
    def __str__(self):
        return str(self.fitness)

class Polynomial(Finch):

    defaults = {
        "ranges":(10,10),
        "mutations":(0.01,0.01)
    }

    def __init__(self, settings):
        super().__init__(settings)

        args = dict(Polynomial.defaults)
        args.update(settings)
        
        self.mutations = args["mutations"]
        self.shape = []

        for r in args["ranges"]:
            self.shape.append(uniform(-r, r))
    
    def react(self, inputs):
        answer = np.zeros(inputs.shape)
        for i in range(len(self.shape)):
            answer += self.shape[i] * (inputs**i)
        return answer
    
    def mutate(self):
        for i in range(len(self.shape)):
            self.shape[i] += uniform(-self.mutations[i], self.mutations[i])
    
    def __str__(self):
        return str(self.fitness) + str([round(i,2) for i in self.shape])

class NeuralNetwork(Finch):

    defaults = {
        "shape":(
            1,
            1
        ),
        "activation":galapagos.activations.sigmoid,
        "memory":0,
        "mutation":0.01
    }

    def __init__(self, settings):
        super().__init__(settings)

        args = dict(NeuralNetwork.defaults)
        args.update(settings)

        self.activation = args["activation"]
        self.mutation = args["mutation"]
        self.memory_size = args["memory"]

        self.shape = []
        for layer in args["shape"]:
            if type(layer) == tuple:
                self.shape.append(randint(layer[0], layer[1]))
            else:
                self.shape.append(layer)
        
        self.synapses = []
        for i in range(len(self.shape)-1):
            self.synapses.append(
                np.random.random((self.shape[i]+self.memory_size if i == 0 else self.shape[i], self.shape[i+1])) * 2 - 1
            )

        
        self.memory_synapses = np.random.random((self.shape[0]+self.memory_size, self.memory_size))
        self.memory = None
    
    def forget(self):
        self.memory = None
    
    def react(self, inputs):
        if self.memory is None:
            self.memory = np.zeros((inputs.shape[0], self.memory_size))
        inputs = np.append(inputs, self.memory, axis=1)
        self.memory = self.activation(np.dot(inputs, self.memory_synapses))
        for s in self.synapses:
            inputs = self.activation(np.dot(inputs, s))
        return inputs
    
    def mutate(self):
        for s in self.synapses:
            s += np.random.random(s.shape)*2*self.mutation - self.mutation
        self.memory_synapses += np.random.random(self.memory_synapses.shape)*2*self.mutation-self.mutation

    def __str__(self):
        return str(self.fitness) + " " + str(self.shape) + " " + str(self.memory_size)


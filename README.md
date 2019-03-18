# assorted-projects
Abandon hope all ye who enter the land of incomplete, uncommented, and undocumented spaghetti code...

Instead of uploading all my code, I have linked to a fantastic online IDE called [repl.it](https://repl.it/).

## Particle Simulation (Javascript)
Simulates perfect kinematic collisions of particles in a box. Parameters in the "canvas.js" file can be tweaked as wanted.

[Try it here](https://repl.it/@mileswatson/ParticleSimulation)

## Complex Function Animator (Python)
Animates complex functions, as given by the function "f(z)" in "main.py". Paramaters can be tweaked under the "grid.animate()"  function. Performance is not great in the repl.it environment, Pygame runs much more smoothly locally.

[Try it here](https://repl.it/@mileswatson/complex-functions)

## Evolution Simulator (Python)
A library that can be used as a framework to simulate evolution, based entirely on an overarching reference to the work of Charles Darwin. "Finches" live on "Islands" which ".pressure()" the finches, before undergoing ".select()"-ion. 

Finches should be implimented by the user, but I have including the "NeuralNetwork(Finch)" class to represent numpy-based RNNs and a simple "Polynomial(Finch)" class too represent a polynomial. Sigmoid and Relu non-linear activation functions are available to use by default.

Finches only have two criteria:
1. They must have a ".react()" function, that takes in a numpy array of inputs, and returns a numpy array of responses.
2. They must have a ".mutate()" function that tweaks the parameters of the instance.

User created Islands should override the default ".test()" function, to allow custom training environments. In my example, I created a neural network that learns to play a simplified version of "Snake".

You can try it [here](https://repl.it/@mileswatson/py-galapagos)

## Sharp Learning Kit (C#)
A neural network library made from scratch in C#. Don't ask me how it works, apparently I didn't know comments existed in 2018.

The limitations are as such:
1. Network structures must be feedforward.
2. Sigmoid is the only supported activation function
3. I don't have a GPU on my laptop, and so this was optimised to use one dimensional arrays instead of multidimensional or jagged arrays. GPU accelerated training is not supported.

[Please don't try it here](https://repl.it/@mileswatson/neural-network-library)

## Compression (Python)
A simple implimentation of the LZ78 (?) compression algorithm. There wasn't much about this online, I kind of had to make it up as I went along.

I think I have a separate repo explaining this in greater detail? Anyway, it is linked below.

[Lunk](https://repl.it/@mileswatson/lempel-ziv-compression)

## Travelling Salesman (Javascript)
Solves a random travelling salesman problem. Uses my own algorithm that swaps edges (because something something triangle inequality something something). I later found out that this was the well known 2-opt algorithm.

## TCS-Oxford Computing Challenge mentorship stuff
Some random stuff I wrote to solve problems in preparation for the BIO. Some of the questions were quite specialised, the solutions may not make much sense on its own.
[Knights Tour Problem in Swift](https://repl.it/@teamproject/swift-knights-tour)
[Wave Simulation Thing](https://repl.it/@teamproject/go-wave-simulation)
[Polynomials](https://repl.it/@teamproject/go-polynomials)
[Heap Optimised Dijkstra's Shortest Path](https://repl.it/@teamproject/go-shortest-paths)
[Above but in python](https://repl.it/@teamproject/py-shortest-paths)

## PoC Blockchain
Some really detailed comments here. Not really sure what the aim of this was, but it outputs true so it probably works?
[See for your self](https://repl.it/@teamproject/go-blockchain)


## CompressionEncryptionHashing
Not really sure what this was, something about compression, encrypting it, and then hashing it I think.

[Lonk](https://repl.it/@mileswatson/CompressionEncryptionHashing)

## Compiler
POCCL = Proof Of Concept Compiled Language. Beginning of explanation in a separate repo.


[Not finished yet, please don't judge.](https://repl.it/@mileswatson/POCCL)



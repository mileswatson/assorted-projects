# assorted-projects
Abandon hope all ye who enter the land of incomplete, uncommented, and undocumented spaghetti code...
Here are some highlights of my programming history...

For some of the projects, I have linked to a fantastic online IDE called [repl.it](https://repl.it/).

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

## TCS-Oxford Computing Challenge mentorship stuff (Assorted)
Some random stuff I wrote to solve problems in preparation for the BIO. Some of the questions were quite specialised, the solutions may not make much sense on its own.

[Knights Tour Problem in Swift](https://repl.it/@teamproject/swift-knights-tour)

[Wave Simulation Thing](https://repl.it/@teamproject/go-wave-simulation)

[Polynomials](https://repl.it/@teamproject/go-polynomials)

[Heap Optimised Dijkstra's Shortest Path](https://repl.it/@teamproject/go-shortest-paths)

[Above but in python](https://repl.it/@teamproject/py-shortest-paths)

## BrainFuckSimplified (Python)
Made a language that allows you to write concise and optimised Brainfuck code, because I needed more headaches in my life. Not sure how it worked, but it did.

[Demo](https://repl.it/@teamproject/CompileBFS)

## Morse Code Radio (Python)
Made a thing to communicate using radio between to RPis. Not sure where the recieving code is, but the sending code works:

[Lenk](https://repl.it/@teamproject/morse-radio)

## A-Star Search Algorithm
Self explanatory...
[Lank](https://repl.it/@teamproject/aStar)

## PoC Blockchain (Go)
Some really detailed comments here. Not really sure what the aim of this was, but it outputs true so it probably works?
[See for your self](https://repl.it/@teamproject/go-blockchain)

## RSA Encryption from Scratch (Java)
An implimentation of an RSA key generation, encryption, and decryption algorithms. My first Java program.

[Its behind you](https://repl.it/@mileswatson/java-crypter)

[Key generation, my first C++ Program](https://repl.it/@mileswatson/RSA-Key-Generation)

## SignMyFile(Python)
Random program that uses homemade RSA cryptography to sign a file.

[REPL Link](https://repl.it/@teamproject/SignMyFile)

## Neural Network in Pure (Python)
Before I knew about OOP and the map function in Python.
[Try before you buy](https://repl.it/@teamproject/Vanilla-Neural-Network)

## GCSE Sort/Search Algorithms
[See them here](https://repl.it/@teamproject/searchSort)

## CompressionEncryptionHashing (Python)
Not really sure what this was, something about compression, encrypting it, and then hashing it I think.

[Lonk](https://repl.it/@mileswatson/CompressionEncryptionHashing)

## Data Interpreter V2 (Python)
The second edition of my famous data interpreter. Don't know / want to know what it actually interprets, but it does.
[No returns](https://repl.it/@mileswatson/Data-Interpreter-V2)

## My Custom Hashing Function
Practically unbreakable, looking back I see no flaws in this algorithm whatsoever.

[Use this in commercial software if you like lawsuits](https://repl.it/@teamproject/Random-hash-function)

## Bank System
I cringe looking back at this, it uses a homemade RSA algorithm and can't save the user data.

[Shield your eyes](https://repl.it/@teamproject/BankSystem)

## Q&A
A very old attempt at understanding Siri/other voice assistants. Attempts to switch possession (my->your).
[AI is just if statements](https://repl.it/@teamproject/Questions)

## Game Of Life (Python)
[Here](https://repl.it/@teamproject/GameOfLife)

## Compiler (Python)
POCCL = Proof Of Concept Compiled Language. Beginning of explanation in a separate repo. It will compile code to NASM, use the NASM assembler, then link with GCC (might be able to get C interoperability working, fingers crossed).

[Not finished yet, please don't judge.](https://repl.it/@mileswatson/POCCL)



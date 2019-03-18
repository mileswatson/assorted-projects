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

Finches should be implimented by the user, but I have including the "NeuralNetwork(Finch)" class to represent numpy-based RNNs and a simple "Polynomial(Finch)" class too represent a polynomial.

Finches only have two criteria:
1. They must have a ".react()" function, that takes in a numpy array of inputs, and returns a numpy array of responses.
2. They must have a ".mutate()" function that tweaks the parameters of the instance.

User created Islands should override the default ".test()" function, to allow custom training environments. In my example, I created a neural network that learns to play a simplified version of "Snake".

You can try it [here](https://repl.it/@mileswatson/py-galapagos)

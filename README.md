# Monopoly: Markov Generator Steady State
This repository contains some basic code for calculating the steady state vector for the per-turn Markov Generator.

I wrote the basic infrastructure for playing the game, even though I was mainly interested in calculating just the Markov Generator. 
Thus, the infrastructure requires some polishing and minor fixes, but the interface is pretty much there.

I based the code on the Euro edition, therefore the naming convention is different from the classic one. The list of the chance and 
community chest cards has been taken from the UK edition as I didn't find the list on the web, and some cards are missing. This changes
a bit the long-run probability, but again, the main infrastructure is there.

The estimation of the per-turn Markov Generator is obtained by means of the Monte Carlo simulation, instead of carefully calculating all the probabilities.
The long-run generator is then calculating exponentiang the stochastic kernel, as the pre-turn kernel should be very close to the theoretical one.

The implementation is split into the following modules:
- Game Engine: where the actual game logic is implemented;
- Monte Carlo Engine: where the callback after every turn is used for updating the Markov Generator.

The Markov Generator is estimated simulating 100,000 scenarios starting from every initial position on the board (except the "Go To" card).
This is done calling the "make_markov_generator" method, which then saves it into the "Data" folder.

Once this is done I plot the bar chart of the Probability Distribution Function. The result is the following:

<p align="center">
  <img src="https://raw.githubusercontent.com/pmontalb/MonopolyMarkovChains/master/Data/steadyStateProbabilities.png">
</p>

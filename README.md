# Elevator-Algorithms
An elevator simulator designed for testing algorithms that carry passengers to their destinations.


The program is a parameterizable elevator system simulator that uses different algorithms for deciding how elevators move between floors.
A time-based simulation is used, for which the state of the simulation is updated in rounds. 
  - Each round represents a fixed length of time (Ex: 1 second).

The context of our elevator simulation is a building, which has:
  - A specified number of floors (numbered starting at Floor 1) 
  - Elevators that can move between each floor
 People can arrive at the elevators at any floor, and elevators move to pick up people and take them to their desired destination floor.
 
People:

Every round of the simulation, zero or more new people arrive at the elevators.
A person in the simulation has three characteristics: 
  - Which floor they started on
  - Which floor they want to go to
  - The number of simulation rounds they have been waiting to reach their target floor. 
The building’s floors are numbered starting at 1. 
Each person’s starting and target floor should be between 1 and the maximum floor number of the building, inclusive.

Elevators:

The simulation has a fixed number of elevators that all begin the simulation at Floor 1 of the building. 
  - An elevator can move one floor (up or down) per simulation round. 
  - So we only need to track which floor each elevator is on, and don’t need to worry about an elevator being “between floors”. 
  - Each elevator keeps track of its passengers (which people are currently on it) and its maximum capacity
  - If an elevator is full, no more people can board it. 
  - Each elevator must be able to track the order in which people boarded it.

Arrival generation algorithms:

At the start of each simulation round, new people may arrive at the elevators. 
There are different ways to decide how many people arrive at a given round, and the starting and target floors of each person.

Random generation:

Each round, a fixed number of people are randomly generated. 
Their starting and target floors are all random, with the requirement that a person’s starting and target floor can’t be the same.

Generation from file data:

Our second approach for arrival generation is to read arrivals from a csv file, in the following format:

Each line of the file represents all of the arrivals for a certain round number.
  - On a single line, the first value is the round number that this line specifies. 
  - This is followed by an even number of other entries, divided into pairs of numbers. 
  - In each pair, the first number is the starting floor and the second number is the target floor of a new arrival. 
  - The arrivals occur in the order the pairs appear in the line. 
  - Each line must have at least one pair (i.e., store at least one new arrival).
  
For example, the following data file

1, 1, 4, 5, 3
3, 1, 2
5, 4, 2
represents the following arrivals:

Round 1: one person whose starting floor is 1 and target floor is 4, and another person whose starting floor is 5 and target floor is 3, in that order.
Round 3: one person whose starting floor is 1 and target floor is 2.
Round 5: one person whose starting floor is 4 and target floor is 2.

Preconditions:

The round numbers are non-negative, and are less than the maximum number of rounds in the simulation. (Note: round numbers start at zero, not one.)
Each round number is unique (no two lines start with the same number). But don’t assume that the lines are in any particular order.
Each person has starting and target floors that are positive, and do not exceed the maximum number of floors in the simulation.
Each person has a target floor that’s different from their starting floor.

Elevator moving algorithms
Each round, an elevator moving algorithm makes a decision about where each elevator should move. 
Because an elevator can only move one floor per round, this decision can have one of three outputs: 
  - The elevator should move up, move down, or stay in the same location.

A moving algorithm receives as input two values:
  - A list of all the elevators in the simulation
  - A dictionary mapping floor numbers to a list of people who are waiting on that floor. 
It outputs a list of decisions (one for each elevator) specifying in which direction it should move.

This is an extremely flexible model of how elevators move (in real-life, the use of elevator buttons makes this much more constrained).


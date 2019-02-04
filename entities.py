"""CSC148 Assignment 1 - People and Elevators

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains classes for the two "basic" entities in this simulation:
people and elevators. We have provided basic outlines of these two classes
for you; you are responsible for implementing these two classes so that they
work with the rest of the simulation.

You may NOT change any existing attributes, or the interface for any public
methods we have provided. However, you can (and should) add new attributes,
and of course you'll have to implement the methods we've provided, as well
as add your own methods to complete this assignment.

Finally, note that Person and Elevator each inherit from a kind of sprite found
in sprites.py; this is to enable their instances to be visualized properly.
You may not change sprites.py, but are responsible for reading the documentation
to understand these classes, as well as the abstract methods your classes must
implement.
"""
from __future__ import annotations
from typing import List
from sprites import PersonSprite, ElevatorSprite


class Elevator(ElevatorSprite):
    """An elevator in the elevator simulation.

    Remember to add additional documentation to this class docstring
    as you add new attributes (and representation invariants).

    === Attributes ===
    passengers: A list of the people currently on this elevator

    === Representation invariants ===
    """
    passengers: List[Person]
    current_floor: int
    max_capacity: int

    def __init__(self, capacity: int) -> None:
        ElevatorSprite.__init__(self)
        self.current_floor = 1
        self.max_capacity = capacity
        self.passengers = []

    def get_floor(self) -> int:
        """Returns the current floor of the elevator."""
        return self.current_floor

    def get_passengers(self) -> List[Person]:
        """Returns the list of passengers in the elevator."""
        return self.passengers

    def is_not_full(self) -> bool:
        """Checks whether the elevator is full."""
        return len(self.passengers) != self.max_capacity

    def is_empty(self) -> bool:
        """Checks if the elevator is empty."""
        return len(self.get_passengers()) == 0

    def add_passenger(self, passenger: Person) -> None:
        """Adds the person to the list of passengers for the elevator."""
        self.passengers.append(passenger)

    def fullness(self) -> float:
        """Return the fraction that this elevator is filled.

        The value returned should be a float between 0.0 (completely empty) and
        1.0 (completely full).
        """
        return len(self.passengers) / self.max_capacity

    def move_up(self) -> None:
        """Increases the current floor by one."""
        self.current_floor += 1

    def move_down(self) -> None:
        """Decreases the current floor by one."""
        self.current_floor -= 1


class Person(PersonSprite):
    """A person in the elevator simulation.

    === Attributes ===
    start: the floor this person started on
    target: the floor this person wants to go to
    wait_time: the number of rounds this person has been waiting

    === Representation invariants ===
    start >= 1
    target >= 1
    wait_time >= 0
    """
    start: int
    target: int
    wait_time: int

    def __init__(self, start: int, target: int) -> None:
        self.wait_time = 0
        PersonSprite.__init__(self)
        self.start = start
        self.target = target

    def get_starting_floor(self) -> int:
        """Returns the starting floor of the person."""
        return self.start

    def get_target_floor(self) -> int:
        """Returns the target floor of the person."""
        return self.target

    def get_wait_time(self) -> int:
        """Returns how many rounds this person has waited."""
        return self.wait_time

    def get_anger_level(self) -> int:
        """Return this person's anger level.

        A person's anger level is based on how long they have been waiting
        before reaching their target floor.
            - Level 0: waiting 0-2 rounds
            - Level 1: waiting 3-4 rounds
            - Level 2: waiting 5-6 rounds
            - Level 3: waiting 7-8 rounds
            - Level 4: waiting >= 9 rounds
        """
        anger_level = [[0, 1, 2], [3, 4], [5, 6], [7, 8]]
        for index, level in enumerate(anger_level):
            if self.wait_time in level:
                return index
        return 4

    def increase_wait_time(self) -> None:
        """Increases the number of waited rounds by one."""
        self.wait_time += 1


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['sprites'],
        'max-nested-blocks': 4,
        'disable': ['R0201'],
        'max-attributes': 12
    })

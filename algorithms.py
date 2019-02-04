"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithms'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional

from entities import Person, Elevator


###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError

    def generate_new_arrivals(self,
                              people: List[Person]) -> Dict[int, List[Person]]:
        """Returns a dictionary of new arrivals based on the people generated
        """
        new_arrivals = {}

        for person in people:
            if person.get_starting_floor() in new_arrivals:
                new_arrivals[person.start].append(person)
            else:
                new_arrivals[person.start] = [person]

        return new_arrivals


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.
    """

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        ArrivalGenerator.__init__(self, max_floor, num_people)

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        """
        if self.num_people is None:
            return {}

        people = self.generate_people()
        return ArrivalGenerator.generate_new_arrivals(self, people)

    def generate_people(self) -> List[Person]:
        """
        Return a list of people with randomly generated
        starting and target floors

        """
        people = []
        possible_floors = list(range(1, self.max_floor + 1))

        for _ in range(self.num_people):
            rand_floors = random.sample(possible_floors, 2)
            people.append(Person(rand_floors[0], rand_floors[1]))
        return people


class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.

    === Attributes ===
    csv:
        A dictionary representing new arrivals based on the CSV file.
        The keys represent the round numbers.
        The values contain a list of starting and target floor pairs.
    """

    csv: Dict[int, List[int]]

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.
        """
        ArrivalGenerator.__init__(self, max_floor, None)
        self.csv = {}
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                round_int = []
                for i in line:
                    if not i.isalpha() and not len(i) == 0:
                        round_int.append(int(i))
                self.csv[round_int[0]] = round_int[1:]

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        """
        if round_num not in self.csv:
            return {}

        people = self.generate_people(round_num)
        return ArrivalGenerator.generate_new_arrivals(self, people)

    def generate_people(self, round_num: int) -> List[Person]:
        """Returns a list of generated people based on the CSV file format
        """
        people = []
        for i in range(0, len(self.csv[round_num]), 2):
            people.append(Person(self.csv[round_num][i],
                                 self.csv[round_num][i + 1]))
        return people


###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        raise NotImplementedError

    def check_waiting(self, waiting: Dict[int, List[Person]]) -> bool:
        """Checks whether there are people waiting on at least one floor."""
        no_people_waiting = True
        for floor in waiting:
            if len(waiting[floor]) > 0:
                no_people_waiting = False
                break
        return no_people_waiting


class RandomAlgorithm(MovingAlgorithm):
    """A moving algorithm that picks a random direction for each elevator.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """
        Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        directions = []
        for elevator in elevators:
            if elevator.get_floor() == 1:
                directions.append(random.choice([Direction.STAY, Direction.UP]))
            elif elevator.get_floor() == max_floor:
                directions.append(random.choice([Direction.STAY,
                                                 Direction.DOWN]))
            else:
                directions.append(random.choice([Direction.STAY, Direction.DOWN,
                                                 Direction.UP]))
        return directions


class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """
        Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        directions = []
        for elevator in elevators:
            if elevator.is_empty():
                lowest_floor = self.get_lowest_floor(waiting)
                if lowest_floor == 0:
                    directions.append(Direction.STAY)
                elif lowest_floor < elevator.current_floor:
                    directions.append(Direction.DOWN)
                elif lowest_floor == elevator.current_floor:
                    directions.append(Direction.STAY)
                else:
                    directions.append(Direction.UP)
            else:
                if elevator.passengers[0].target < elevator.current_floor:
                    directions.append(Direction.DOWN)
                elif elevator.passengers[0].target == elevator.current_floor:
                    directions.append(Direction.STAY)
                else:
                    directions.append(Direction.UP)
        return directions

    def get_lowest_floor(self, waiting: Dict[int, List[Person]]) -> int:
        """Returns the lowest floor that has at least one person waiting."""
        for floor, people in sorted(waiting.items()):
            if len(people) > 0:
                return floor
        return 0


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        directions = []
        for elevator in elevators:
            if elevator.is_empty():
                if self.check_waiting(waiting):
                    directions.append(Direction.STAY)
                else:
                    closest_floor = self.empty_closest_floor(elevator,
                                                             waiting,
                                                             max_floor)
                    if closest_floor < elevator.get_floor():
                        directions.append(Direction.DOWN)
                    elif closest_floor == elevator.get_floor():
                        directions.append(Direction.STAY)
                    else:
                        directions.append(Direction.UP)
            else:
                closest_floor = self.closest_target_floor(elevator, max_floor)
                if closest_floor < elevator.get_floor():
                    directions.append(Direction.DOWN)
                elif closest_floor == elevator.get_floor():
                    directions.append(Direction.STAY)
                else:
                    directions.append(Direction.UP)
        return directions

    def empty_closest_floor(self, elevator: Elevator,
                            waiting: Dict[int, List[Person]],
                            max_floor: int) -> int:
        """
        Returns the closest floor to the elevator that contains waiting people.
        This method is designed for empty elevators.
        """
        closest_floor = elevator.get_floor()
        floors_to_check = self.floor_check(elevator, max_floor)
        for floor in floors_to_check:
            if len(waiting[floor]) > 0:
                closest_floor = floor
                break
        return closest_floor

    def floor_check(self, elevator: Elevator, max_floor: int) -> List[int]:
        """
        Returns a list of all possible floors by order of
        closest distance to elevator
        """
        floors = []
        current_floor = elevator.get_floor()
        floors.append(current_floor)
        max_distance = max_floor - 1
        for i in range(1, max_distance + 1):
            floors.append(current_floor - i)
            floors.append(current_floor + i)
        filtered_floors = self.filter_impossible_floors(floors, max_floor)
        return filtered_floors

    def filter_impossible_floors(self, floors: List[int],
                                 max_floor: int) -> List[int]:
        """
        Returns a filtered list of possible floors
        based on the maximum floor.
        """
        filtered_floors = []
        for floor in floors:
            if 0 < floor <= max_floor:
                filtered_floors.append(floor)
        return filtered_floors

    def closest_target_floor(self, elevator: Elevator, max_floor: int) -> int:
        """
        Returns the closest target floor based on
        the elevators current passengers and current floor.
        This method is designed for non-empty elevators.
        """
        closest_floor = elevator.get_floor()
        closest_floors = self.floor_check(elevator, max_floor)
        passenger_floors = []
        for passenger in elevator.get_passengers():
            passenger_floors.append(passenger.get_target_floor())
        for floor in closest_floors:
            if floor in passenger_floors:
                closest_floor = floor
                break
        return closest_floor


if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'disable': ['R0201'],
        'max-attributes': 12
    })

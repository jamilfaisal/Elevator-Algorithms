"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any

import algorithms
from algorithms import Direction
from entities import Person, Elevator
from visualizer import Visualizer


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals.
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    waiting: a dictionary of people waiting for an elevator
             (keys are floor numbers, values are the list of waiting people)
    """
    arrival_generator: algorithms.ArrivalGenerator
    num_of_arrivals: int
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    people_completed: List[Person]
    num_floors: int
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration."""
        self.elevators = []
        for _ in range(config["num_elevators"]):
            self.elevators.append(Elevator(config["elevator_capacity"]))

        self.waiting = {}
        self.num_floors = config["num_floors"]
        self.generate_waiting()

        self.arrival_generator = config["arrival_generator"]
        self.num_of_arrivals = 0
        self.people_completed = []

        self.moving_algorithm = config["moving_algorithm"]
        # Initialize the visualizer.
        # Note that this should be called *after* the other attributes
        # have been initialized.
        self.visualizer = Visualizer(self.elevators,
                                     self.num_floors,
                                     config['visualize'])

    def generate_waiting(self) -> None:
        """Generates self.waiting keys with empty lists for values."""
        for i in range(1, self.num_floors + 1):
            self.waiting[i] = []

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Stage 5: handle people wait time
            self._handle_wait_time()

            # Pause for 1 second
            self.visualizer.wait(1)

        return self._calculate_stats(num_rounds)

    def _generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals."""

        new_arrivals = self.arrival_generator.generate(round_num)
        for key in new_arrivals:
            self.num_of_arrivals += len(new_arrivals[key])
            self.waiting[key].extend(new_arrivals[key])
        self.visualizer.show_arrivals(self.waiting)

    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""
        for elevator in self.elevators:
            leaving_list = elevator.passengers[:]
            for person in leaving_list:
                if person.target == elevator.get_floor():
                    elevator.get_passengers().remove(person)
                    self.visualizer.show_disembarking(person, elevator)
                    self.people_completed.append(person)

    def _handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""
        for key in self.waiting:
            people_copy = self.waiting[key][:]
            for person in people_copy:
                for elevator in self.elevators:
                    if person.get_starting_floor() == elevator.get_floor() \
                            and elevator.is_not_full():
                        elevator.add_passenger(person)
                        self.visualizer.show_boarding(person, elevator)
                        self.waiting[key].remove(person)
                        break

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.

        Use this simulation's moving algorithm to move the elevators.
        """
        directions = self.moving_algorithm.move_elevators(self.elevators,
                                                          self.waiting,
                                                          self.num_floors)
        if len(directions) == 0:
            return None

        for iterator in range(len(self.elevators)):
            if directions[iterator] == Direction.DOWN:
                self.elevators[iterator].move_down()
            elif directions[iterator] == Direction.UP:
                self.elevators[iterator].move_up()
        self.visualizer.show_elevator_moves(self.elevators, directions)
        return None

    def _handle_wait_time(self) -> None:
        """Increases wait_time of people waiting and
         passengers in all elevators"""
        for key in self.waiting:
            for person in self.waiting[key]:
                person.increase_wait_time()
        for elevator in self.elevators:
            for passenger in elevator.get_passengers():
                passenger.increase_wait_time()

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self, num_rounds: int) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """
        return {
            'num_iterations': num_rounds,
            'total_people': self.num_of_arrivals,
            'people_completed': len(self.people_completed),
            'max_time': self.max_time(),
            'min_time': self.min_time(),
            'avg_time': self.avg_time()
        }

    def max_time(self) -> int:
        """Returns the the maximum time someone spent before reaching their
         target floor during the simulation
         (note that this includes time spent waiting on a floor and travelling
          on an elevator)
        """
        max_time = -1
        for person in self.people_completed:
            if person.get_wait_time() > max_time:
                max_time = person.get_wait_time()
        return max_time

    def min_time(self) -> int:
        """Returns the minimum time someone spent before reaching their
         target floor
         """
        if len(self.people_completed) == 0:
            return -1
        min_rounds = self.people_completed[0].get_wait_time()
        for person in self.people_completed:
            if person.get_wait_time() < min_rounds:
                min_rounds = person.get_wait_time()
        return min_rounds

    def avg_time(self) -> int:
        """Returns the average time someone spent before reaching their
         target floor, rounded down to the nearest integer
         """
        if len(self.people_completed) == 0:
            return -1
        total_rounds = 0
        for person in self.people_completed:
            total_rounds += person.get_wait_time()
        average_rounds = int(total_rounds / len(self.people_completed))
        return average_rounds


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 6,
        'num_elevators': 6,
        'elevator_capacity': 3,
        'num_people_per_round': 3,
        # Random arrival generator with 6 max floors and 1 arrival per round.
        # 'arrival_generator': algorithms.RandomArrivals(6, 2),
        'arrival_generator': algorithms.FileArrivals(8, 'sample_arrivals.csv'),
        'moving_algorithm': algorithms.PushyPassenger(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(15)
    return stats


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    print(sample_run())
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
    #     'max-nested-blocks': 4,
    #     'disable': ['R0201'],
    #     'max-attributes': 12
    # })

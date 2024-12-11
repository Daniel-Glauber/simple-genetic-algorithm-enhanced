# Author: Daniel Glauber
# File: individual.py
# Description: Contains the Individual class, which represents a single solution in the population.

# Constants for magic numbers and strings
FITNESS_FUNCTION_SIMPLE = 0
FITNESS_FUNCTION_COMPLEX = 1

# Class Individual represents a single solution in population
class Individual:
    """
    Class Individual represents a single solution in the population.
    """

    def __init__(self, fitness_function: int, starting_solution: list[int] = [], solution_fitness: int = None) -> None:
        """
        Initializes an Individual instance.

        Args:
            fitness_function (int): The fitness function to use.
            starting_solution (list[int], optional): The initial solution. Defaults to [].
            solution_fitness (int, optional): The fitness of the initial solution. Defaults to None.
        """
        self._fitness_function_value = fitness_function
        self._solution = starting_solution.copy()
        self._fitness_evaluated = False
        self._solution_fitness = solution_fitness
        if len(self._solution) > 0:
            self.evaluate_solution_fitness(solution_fitness)

    # Getter and setter for _fitness_function_value
    @property
    def fitness_function_value(self) -> int:
        return self._fitness_function_value

    @fitness_function_value.setter
    def fitness_function_value(self, value: int) -> None:
        self._fitness_function_value = value

    # Getter and setter for _solution
    @property
    def solution(self) -> list[int]:
        return self._solution

    @solution.setter
    def solution(self, solution: list[int]) -> None:
        self._solution = solution.copy()
        self._fitness_evaluated = False

    # Getter and setter for _fitness_evaluated
    @property
    def fitness_evaluated(self) -> bool:
        return self._fitness_evaluated

    @fitness_evaluated.setter
    def fitness_evaluated(self, evaluated: bool) -> None:
        self._fitness_evaluated = evaluated

    # Getter for _solution_fitness
    @property
    def solution_fitness(self) -> int:
        if self._fitness_evaluated:
            return self._solution_fitness
        else:
            self.evaluate_solution_fitness()
            return self._solution_fitness

    def get_fitness_function_value(self) -> int:
        """
        Returns the fitness function value.

        Returns:
            int: The fitness function value.
        """
        return self._fitness_function_value

    def set_fitness_function_value(self, value: int) -> None:
        """
        Sets the fitness function value.

        Args:
            value (int): The fitness function value to set.
        """
        self._fitness_function_value = value

    def get_solution(self) -> list[int]:
        """
        Returns the solution.

        Returns:
            list[int]: The solution.
        """
        return self._solution

    def set_solution(self, solution: list[int]) -> None:
        """
        Sets the solution.

        Args:
            solution (list[int]): The solution to set.
        """
        self._solution = solution.copy()
        self._fitness_evaluated = False

    def is_fitness_evaluated(self) -> bool:
        """
        Checks if the fitness has been evaluated.

        Returns:
            bool: True if the fitness has been evaluated, False otherwise.
        """
        return self._fitness_evaluated

    def set_fitness_evaluated(self, evaluated: bool) -> None:
        """
        Sets the fitness evaluated status.

        Args:
            evaluated (bool): The fitness evaluated status to set.
        """
        self._fitness_evaluated = evaluated

    def solution_as_string(self) -> str:
        """
        Returns the solution as a string.

        Returns:
            str: The solution as a string.
        """
        return ",".join([str(x) for x in self._solution])

    def mutate_solution(self, indexes_to_mutate_bool_list: list[bool], full_debug: bool = False) -> None:
        """
        Mutates the solution based on the provided boolean list.

        Args:
            indexes_to_mutate_bool_list (list[bool]): List indicating which indexes to mutate.
            full_debug (bool, optional): Whether to print debug information. Defaults to False.
        """
        if any(indexes_to_mutate_bool_list):
            if full_debug is True:
                print(f"Before Mutation: {self.solution_as_string()}")
            for index, mutate_boolean in enumerate(indexes_to_mutate_bool_list):
                if mutate_boolean is True:
                    # XOR operation to flip the bit (0 to 1 or 1 to 0)
                    self._solution[index] = self._solution[index] ^ 1
            self.evaluate_solution_fitness()
            if full_debug is True:
                print(f"After Mutation: {self.solution_as_string()}\n")

    def evaluate_solution_fitness(self, solution_fitness: int = None) -> None:
        """
        Evaluates the fitness of the solution.

        Args:
            solution_fitness (int, optional): The fitness value to set. Defaults to None.
        """
        if solution_fitness is not None:
            self._solution_fitness = solution_fitness
        else:
            if self._fitness_function_value == FITNESS_FUNCTION_SIMPLE:
                # Simple fitness function: sum of the solution elements
                self._solution_fitness = sum(self._solution)
                self._fitness_evaluated = True
            elif self._fitness_function_value == FITNESS_FUNCTION_COMPLEX:
                # Complex fitness function: sum of fitness values from a lookup table
                fitness_lookup = {
                    0: 3,
                    1: 2,
                    2: 1,
                    3: 0,
                    4: 4
                }
                # Partition the solution into chunks of 4 and sum their fitness values
                self._solution_fitness = sum([fitness_lookup[sum(partition)]
                                             for partition in
                                             (self._solution[i:i+4]
                                              for i in
                                              range(0, len(self._solution), 4))])
                self._fitness_evaluated = True

    def get_solution_fitness(self) -> int:
        """
        Returns the fitness of the solution.

        Returns:
            int: The fitness of the solution.
        """
        if self._fitness_evaluated is True:
            return self._solution_fitness
        else:
            self.evaluate_solution_fitness()
            return self._solution_fitness

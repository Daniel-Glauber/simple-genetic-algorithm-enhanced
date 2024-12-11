# Author: Daniel Glauber
# File: population.py
# Description: Contains the Population class, which represents the entire population of individual solutions.
import copy
import random
import logging
from operator import attrgetter
from individual import Individual
import settings_loader as sl
from typing import List, Tuple, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for magic numbers and strings
SELECTION_METHOD_TOURNAMENT = 0
CROSSOVER_OPERATOR_UNIFORM = 0
CROSSOVER_OPERATOR_ONE_POINT = 1
CROSSOVER_OPERATOR_TWO_POINT = 2
FULL_DEBUG = True
LIMITED_DEBUG = True

# Class Population represents the entire population of individual solutions.
class Population:
    """
    Class Population represents the entire population of individual solutions.
    """
    def __init__(self):
        """
        Initializes the Population with settings loaded from the settings_loader.
        """
        self._fitnessFunction = sl.get_setting("fitnessFunction")
        self._current_generation = []
        self._next_generation = []
        self._full_debug = sl.get_setting("fullDebug")
        self._limited_debug = sl.get_setting("limitedDebug")
        self._string_size = sl.get_setting("stringSizeN")
        self._population_size = sl.get_setting("populationSizeN")
        self._selectionMethod = sl.get_setting("selectionMethod")
        self._probApplyCrossover = sl.get_setting("probApplyCrossover")
        self._crossoverOperator = sl.get_setting("crossoverOperator")
        self._probApplyMutation = sl.get_setting("probApplyMutation")
        self._tournament_selection_size = sl.get_setting("tournamentSizeK")
        self._failures_before_termination = sl.get_setting("failuresBeforeTermination")

    # Getter and Setter methods
    @property
    def current_generation(self):
        return self._current_generation

    @current_generation.setter
    def current_generation(self, value):
        self._current_generation = value

    @property
    def next_generation(self):
        return self._next_generation

    @next_generation.setter
    def next_generation(self, value):
        self._next_generation = value

    @property
    def full_debug(self):
        return self._full_debug

    @full_debug.setter
    def full_debug(self, value):
        self._full_debug = value

    @property
    def limited_debug(self):
        return self._limited_debug

    @limited_debug.setter
    def limited_debug(self, value):
        self._limited_debug = value

    @property
    def string_size(self):
        return self._string_size

    @string_size.setter
    def string_size(self, value):
        self._string_size = value

    @property
    def population_size(self):
        return self._population_size

    @population_size.setter
    def population_size(self, value):
        self._population_size = value

    @property
    def selectionMethod(self):
        return self._selectionMethod

    @selectionMethod.setter
    def selectionMethod(self, value):
        self._selectionMethod = value

    @property
    def probApplyCrossover(self):
        return self._probApplyCrossover

    @probApplyCrossover.setter
    def probApplyCrossover(self, value):
        self._probApplyCrossover = value

    @property
    def crossoverOperator(self):
        return self._crossoverOperator

    @crossoverOperator.setter
    def crossoverOperator(self, value):
        self._crossoverOperator = value

    @property
    def probApplyMutation(self):
        return self._probApplyMutation

    @probApplyMutation.setter
    def probApplyMutation(self, value):
        self._probApplyMutation = value

    @property
    def tournament_selection_size(self):
        return self._tournament_selection_size

    @tournament_selection_size.setter
    def tournament_selection_size(self, value):
        self._tournament_selection_size = value

    @property
    def failures_before_termination(self):
        return self._failures_before_termination

    @failures_before_termination.setter
    def failures_before_termination(self, value):
        self._failures_before_termination = value

    def initialize_random_individual(self, string_size: int) -> Individual:
        """
        Initializes a random individual with a given string size.

        Args:
            string_size (int): The size of the individual's solution string.

        Returns:
            Individual: A new individual with a random solution.
        """
        # Generate a random binary solution of the given size
        starting_solution = [random.randint(0, 1) for i in range(0, string_size)]
        return Individual(self._fitnessFunction, starting_solution)

    def initialize_random_starting_population(self) -> None:
        """
        Initializes the starting population with random individuals.
        """
        # Reset current and next generations
        self.current_generation = []
        self.next_generation = []
        # Seed the random number generator for reproducibility
        random.seed(sl.get_setting("randSeed"))
        # Load settings from the settings loader
        self.full_debug = sl.get_setting("fullDebug")
        self.limited_debug = sl.get_setting("limitedDebug")
        self.string_size = sl.get_setting("stringSizeN")
        self.population_size = sl.get_setting("populationSizeN")
        self.selectionMethod = sl.get_setting("selectionMethod")
        self.probApplyCrossover = sl.get_setting("probApplyCrossover")
        self.crossoverOperator = sl.get_setting("crossoverOperator")
        self.probApplyMutation = sl.get_setting("probApplyMutation")
        self.tournament_selection_size = sl.get_setting("tournamentSizeK")
        self.failures_before_termination = sl.get_setting("failuresBeforeTermination")
        # Initialize the current generation with random individuals
        self.current_generation = [self.initialize_random_individual(self.string_size) for i in range(self.population_size)]
        # Log the initial population if debugging is enabled
        if self.full_debug == FULL_DEBUG or self.limited_debug == LIMITED_DEBUG:
            logger.info("Initial Population")
            temp_population = copy.deepcopy(self.current_generation)
            for i in temp_population:
                logger.info(f"{i.solution_as_string()}")

    def get_average_fitness(self) -> float:
        """
        Calculates the average fitness of the current generation.

        Returns:
            float: The average fitness of the current generation.
        """
        # Calculate the average fitness of all individuals in the current generation
        self.current_average_fitness = (sum(individual.get_solution_fitness() for individual in self.current_generation) / sl.get_setting("populationSizeN"))
        return self.current_average_fitness

    def get_worst_fitness(self) -> Dict[str, float]:
        """
        Finds the individual with the worst fitness in the current generation.

        Returns:
            Dict[str, float]: A dictionary containing the worst individual's fitness, solution, and index.
        """
        # Find the individual with the lowest fitness
        worst_individual = min(self.current_generation, key=attrgetter('_solution_fitness'))
        worst_index = self.current_generation.index(worst_individual)
        worst_data = {
            "fitness": worst_individual.get_solution_fitness(),
            "solution": worst_individual.get_solution(),
            "index": worst_index
        }
        return worst_data

    def get_best_fitness(self) -> Dict[str, float]:
        """
        Finds the individual with the best fitness in the current generation.

        Returns:
            Dict[str, float]: A dictionary containing the best individual's fitness, solution, and index.
        """
        # Find the individual with the highest fitness
        best_individual = max(self.current_generation, key=attrgetter('_solution_fitness'))
        best_index = self.current_generation.index(best_individual)
        best_data = {
            "fitness": best_individual.get_solution_fitness(),
            "solution": best_individual.get_solution(),
            "index": best_index
        }
        return best_data

    def single_tournament_selection(self) -> Tuple[Individual, Individual]:
        """
        Selects two parents using tournament selection.

        Returns:
            Tuple[Individual, Individual]: A tuple containing two selected parents.
        """
        # Select two parents using the tournament selection method
        return (self.single_parent_selection(), self.single_parent_selection())

    def single_parent_selection(self) -> Individual:
        """
        Selects a single parent using tournament selection.

        Returns:
            Individual: The selected parent.
        """
        # Randomly select a subset of individuals for the tournament
        selection = random.choices(self.current_generation, k=self.tournament_selection_size)
        # Choose the individual with the best fitness from the selection
        best_parent = max(selection, key=attrgetter('_solution_fitness'))
        if self.full_debug == FULL_DEBUG:
            logger.info("Selecting parent")
            logger.info('\n'.join([(f"{parent.solution_as_string()}, Fitness: {parent.solution_fitness}") for parent in selection]))
            logger.info(f"Selected parent: {best_parent.solution_as_string()}\n")
        return best_parent

    def tournament_selection(self, empty: int) -> List[Individual]:
        """
        Performs tournament selection to generate children.

        Args:
            empty (int): A placeholder argument.

        Returns:
            List[Individual]: A list of generated children.
        """
        # Select parents and perform crossover to generate children
        parents_tuple = self.single_tournament_selection()
        children = self.crossover_controller(parents_tuple)
        # Attempt to mutate each child
        [self.attempt_mutation(child) for child in children]
        return children

    def attempt_mutation(self, child: Individual) -> None:
        """
        Attempts to mutate a given child.

        Args:
            child (Individual): The child to mutate.
        """
        # Mutate the child with a certain probability
        if random.random() < self.probApplyMutation:
            indexes_to_mutate_bool_list = [random.random() < 1/self.string_size for i in range(self.string_size)]
            if self.full_debug:
                child.mutate_solution(indexes_to_mutate_bool_list, True)
            else:
                child.mutate_solution(indexes_to_mutate_bool_list)

    def crossover_controller(self, parents_tuple: Tuple[Individual, Individual]) -> List[Individual]:
        """
        Controls the crossover process based on the selected crossover operator.

        Args:
            parents_tuple (Tuple[Individual, Individual]): A tuple containing two parent individuals.

        Returns:
            List[Individual]: A list of generated children.
        """
        # Dictionary mapping crossover operators to their respective functions
        crossover_functions = {
            CROSSOVER_OPERATOR_UNIFORM: self.uniform_crossover,
            CROSSOVER_OPERATOR_ONE_POINT: self.one_point_crossover,
            CROSSOVER_OPERATOR_TWO_POINT: self.two_point_crossover
        }
        # Perform the selected crossover operation
        return crossover_functions[self.crossoverOperator](parents_tuple)

    def one_point_crossover(self, parents_tuple: Tuple[Individual, Individual]) -> List[Individual]:
        """
        Performs one-point crossover on the given parents.

        Args:
            parents_tuple (Tuple[Individual, Individual]): A tuple containing two parent individuals.

        Returns:
            List[Individual]: A list of generated children.
        """
        # Extract solutions from parents
        parents_solution_tuple = (parents_tuple[0]._solution, parents_tuple[1]._solution)
        if self.full_debug == FULL_DEBUG:
            logger.info("Before One-Point Crossover")
            logger.info(f"p1: {parents_tuple[0].solution_as_string()}")
            logger.info(f"p2: {parents_tuple[1].solution_as_string()}")

        if random.random() < self.probApplyCrossover:
            # Select a crossover point and create children by swapping segments
            crossover_index = random.randrange(0, self.string_size)
            if self.full_debug == FULL_DEBUG:
                logger.info(f"Crossover Point: {crossover_index}")
            child_a = (parents_solution_tuple[0][0:crossover_index] + parents_solution_tuple[1][crossover_index::])
            child_b = (parents_solution_tuple[1][0:crossover_index] + parents_solution_tuple[0][crossover_index::])
            children = [Individual(self._fitnessFunction, child_a), Individual(self._fitnessFunction, child_b)]
            if self.full_debug == FULL_DEBUG:
                logger.info("After One-Point Crossover")
                logger.info(f"c1: {children[0].solution_as_string()}")
                logger.info(f"c2: {children[1].solution_as_string()}\n")
            return children
        else:
            # If crossover is not applied, return copies of the parents
            children = [(Individual(self._fitnessFunction, parents_tuple[0]._solution, parents_tuple[0]._solution_fitness)),
                        (Individual(self._fitnessFunction, parents_tuple[1]._solution, parents_tuple[1]._solution_fitness))]
            if self.full_debug == FULL_DEBUG:
                logger.info("After One-Point Crossover")
                logger.info(f"c1: {children[0].solution_as_string()}")
                logger.info(f"c2: {children[1].solution_as_string()}\n")
            return children

    def two_point_crossover(self, parents_tuple: Tuple[Individual, Individual]) -> List[Individual]:
        """
        Performs two-point crossover on the given parents.

        Args:
            parents_tuple (Tuple[Individual, Individual]): A tuple containing two parent individuals.

        Returns:
            List[Individual]: A list of generated children.
        """
        # Extract solutions from parents
        parents_solution_tuple = (parents_tuple[0]._solution, parents_tuple[1]._solution)
        if self.full_debug == FULL_DEBUG:
            logger.info("Before Two-Point Crossover")
            logger.info(f"p1: {parents_tuple[0].solution_as_string()}")
            logger.info(f"p2: {parents_tuple[1].solution_as_string()}")

        if random.random() < self.probApplyCrossover:
            # Select two crossover points and create children by swapping segments
            crossover_indexes = [random.randrange(0, self.string_size), random.randrange(0, self.string_size)]
            crossover_indexes.sort()
            if self.full_debug == FULL_DEBUG:
                logger.info(("Crossover Points: " + ", ".join([str(index) for index in crossover_indexes])))
            child_a = (parents_solution_tuple[0][0:crossover_indexes[0]] + parents_solution_tuple[1][crossover_indexes[0]:crossover_indexes[1]] + parents_solution_tuple[0][crossover_indexes[1]::])
            child_b = (parents_solution_tuple[1][0:crossover_indexes[0]] + parents_solution_tuple[0][crossover_indexes[0]:crossover_indexes[1]] + parents_solution_tuple[1][crossover_indexes[1]::])
            children = [Individual(self._fitnessFunction, child_a), Individual(self._fitnessFunction, child_b)]
            if self.full_debug == FULL_DEBUG:
                logger.info("After Two-Point Crossover")
                logger.info(f"c1: {children[0].solution_as_string()}")
                logger.info(f"c2: {children[1].solution_as_string()}\n")
            return children
        else:
            # If crossover is not applied, return copies of the parents
            children = [(Individual(self._fitnessFunction, parents_tuple[0]._solution, parents_tuple[0]._solution_fitness)),
                        (Individual(self._fitnessFunction, parents_tuple[1]._solution, parents_tuple[1]._solution_fitness))]
            if self.full_debug == FULL_DEBUG:
                logger.info("After Two-Point Crossover")
                logger.info(f"c1: {children[0].solution_as_string()}")
                logger.info(f"c2: {children[1].solution_as_string()}\n")
            return children

    def uniform_crossover(self, parents_tuple: Tuple[Individual, Individual]) -> List[Individual]:
        """
        Performs uniform crossover on the given parents.

        Args:
            parents_tuple (Tuple[Individual, Individual]): A tuple containing two parent individuals.

        Returns:
            List[Individual]: A list of generated children.
        """
        # Extract solutions from parents
        parents_solution_tuple = (parents_tuple[0].get_solution(), parents_tuple[1].get_solution())
        if self.full_debug == FULL_DEBUG:
            logger.info("Before Uniform Crossover")
            logger.info(f"p1: {parents_tuple[0].solution_as_string()}")
            logger.info(f"p2: {parents_tuple[1].solution_as_string()}")

        if random.random() < self.probApplyCrossover:
            # Create children by randomly selecting genes from each parent
            res = [(i, i ^ 1) for i in (random.choice([0, 1]) for i in range(self.string_size))]
            child_a = [parents_solution_tuple[parent[0]][index] for index, parent in enumerate(res)]
            child_b = [parents_solution_tuple[parent[1]][index] for index, parent in enumerate(res)]
            children = [Individual(self._fitnessFunction, child_a), Individual(self._fitnessFunction, child_b)]
            if self.full_debug == FULL_DEBUG:
                logger.info("After Uniform Crossover")
                logger.info(f"c1: {children[0].solution_as_string()}")
                logger.info(f"c2: {children[1].solution_as_string()}\n")
            return children
        else:
            # If crossover is not applied, return copies of the parents
            children = [(Individual(self._fitnessFunction, parents_tuple[0].get_solution(), parents_tuple[0].get_solution_fitness())),
                        (Individual(self._fitnessFunction, parents_tuple[1].get_solution(), parents_tuple[1].get_solution_fitness()))]
            if self.full_debug == FULL_DEBUG:
                logger.info("After Uniform Crossover")
                logger.info(f"c1: {children[0].solution_as_string()}")
                logger.info(f"c2: {children[1].solution_as_string()}\n")
            return children

    def replace_current_population(self) -> None:
        """
        Replaces the current generation with the next generation.
        """
        # Replace the current generation with the next generation
        self.current_generation = []
        self.current_generation = copy.deepcopy(self.next_generation)
        self.next_generation = []

    def select_mating_parents(self) -> None:
        """
        Selects mating parents and generates the next generation.
        """
        # Preserve the best individual from the current generation
        best_individual_data = self.get_best_fitness()
        best_individual = (Individual(self._fitnessFunction, best_individual_data["solution"], best_individual_data["fitness"]))
        if self.selectionMethod == SELECTION_METHOD_TOURNAMENT:
            # Generate new offspring using tournament selection
            new_offspring = map(self.tournament_selection, (i for i in range(self.population_size // 2)))
            for items in new_offspring:
                for child in items:
                    if len(self.next_generation) < self.population_size - 1:
                        self.next_generation.append(child)
            # Add the best individual to the next generation
            self.next_generation.append(best_individual)

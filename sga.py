# Author: Daniel Glauber
# File: sga.py
# Description: This script runs the simple genetic algorithm (SGA) based on the settings provided.
import sys
from population import Population
import settings_loader as sl
import json
import time

# Constants
TERMINATE_ON_FAILURE = "terminateOnFailure"
FAILURES_BEFORE_TERMINATION = "failuresBeforeTermination"
STRING_SIZE_N = "stringSizeN"
FULL_DEBUG = "fullDebug"
BISECTION = "bisection"
BISECTION_THRESHOLD = "bisectionThreshold"
BISECTION_STARTING_POPULATION = "bisectionStartingPopulation"
BISECTION_MAX_GENERATION = "bisectionMaxGeneration"
LIMITED_DEBUG = "limitedDebug"
POPULATION_SIZE_N = "populationSizeN"
SUCCESS = "SUCCESS\n"
FAILED = "FAILED\n"
FAILURES_REMAINING_MSG = "Failures remaining before termination "


class SGAController:
    """
    This class is the controller for the simple genetic algorithm (SGA).
    """

    def __init__(self):
        """
        Initializes the SGAController with settings and initial population.
        """
        # Initialize variables and load settings
        self.saved_generation_data = []
        self.population = Population()
        self.terminate_on_failure = sl.get_setting(TERMINATE_ON_FAILURE) == 1
        self.failures_remaining = sl.get_setting(FAILURES_BEFORE_TERMINATION)
        self.string_size = sl.get_setting(STRING_SIZE_N)
        self.generation_number = 1
        self.full_debug = sl.get_setting(FULL_DEBUG)
        self.bisection_option = sl.get_setting(BISECTION)
        self.bisection_threshold = sl.get_setting(BISECTION_THRESHOLD)
        self.bisection_starting_population = sl.get_setting(
            BISECTION_STARTING_POPULATION)
        self.bisection_max_generation = sl.get_setting(
            BISECTION_MAX_GENERATION)
        self.limited_debug = sl.get_setting(LIMITED_DEBUG)
        self.terminate_run = False

    def get_generation_data(self):
        """
        Collects data for the current generation including best, average, and worst fitness.
        """
        # Gather fitness data for the current generation
        self.generation_data = {}
        self.generation_data["generation"] = self.generation_number
        self.generation_data["best"] = self.population.get_best_fitness()
        self.generation_data["average"] = self.population.get_average_fitness()
        self.generation_data["worst"] = self.population.get_worst_fitness()

    def save_generation_data(self):
        """
        Saves the current generation data and checks for termination conditions.
        
        Returns:
            bool: True if the run needs to be terminated, False otherwise.
        """
        needs_termination = False
        self.get_generation_data()
        # Create a message summarizing the current generation's fitness
        message_array = [f"Generation {self.generation_number}: ",
                         f"(B: {self.generation_data['best']['fitness']},",
                         f"A: {self.generation_data['average']},",
                         f"W: {self.generation_data['worst']['fitness']})"]
        message = ' '.join(message_array)
        self.generation_data['message'] = message
        print(message)
        # Print detailed debug information if enabled
        if self.full_debug or self.limited_debug:
            debug_array = [
                "Current Population",
                '\n'.join([i.solution_as_string()
                           for i in self.population.current_generation]),
                ' '.join(["Best Solution =",
                          (','.join([str(i)
                           for i in self.generation_data['best']['solution']]))]),
                ' '.join(["Worst Solution =",
                          (','.join([str(i)
                           for i in self.generation_data['worst']['solution']])), '\n'])
            ]
            print('\n'.join(debug_array))
        self.saved_generation_data.append(self.generation_data)

        # Check if the best fitness matches the string size, indicating success
        if self.string_size == self.generation_data['best']['fitness']:
            success_array = [
                ' '.join(["Global Best Fitness =",
                          str(self.generation_data['best']['fitness'])]),
                ' '.join(["Global Best Solution =",
                          ','.join([str(i)
                                    for i in self.generation_data['best']['solution']])]),
                ' '.join(["Global Best was at index",
                          str(self.generation_data['best']['index']),
                          "of",
                          str(len(self.population.current_generation))]),
                ' '.join(["Average Fitness:",
                          str(self.generation_data['average'])]),
                ' '.join(["Worst Fitness:",
                          str(self.generation_data['worst']['fitness'])]),
            ]
            print('\n'.join(success_array))
            print(SUCCESS)
            needs_termination = True

        # Check for termination conditions based on failure criteria
        if len(self.saved_generation_data) == 4:
            self.saved_generation_data.pop(0)
            if self.terminate_on_failure:
                for index, data in enumerate(self.saved_generation_data):
                    if index == 0:
                        oldest_gen_best = data["best"]["fitness"]
                        oldest_gen_average = data['average']
                    else:
                        if (data["best"]["fitness"] >= oldest_gen_best and
                                data['average'] > oldest_gen_average):
                            break
                        elif (index == 2 and data["best"]["fitness"] <= oldest_gen_best and
                              data['average'] < oldest_gen_average):
                            if self.failures_remaining == 0:
                                needs_termination = True
                                best_generation = self.saved_generation_data[0]["best"]
                                worst_generation = self.saved_generation_data[0]["worst"]
                                best_average = self.saved_generation_data[0]["average"]
                                worst_average = self.saved_generation_data[0]["average"]
                                for data in self.saved_generation_data:
                                    if data["best"]["fitness"] > best_generation["fitness"]:
                                        best_generation = data["best"]
                                    if data["worst"]["fitness"] < worst_generation["fitness"]:
                                        worst_generation = data["worst"]
                                    if data["average"] < worst_average:
                                        worst_average = data["average"]
                                    if data["average"] > best_average:
                                        best_average = data["average"]
                                failure_array = [
                                    ' '.join(["Best Fitness in previous 3 generations =",
                                              str(best_generation['fitness'])]),
                                    ' '.join(["Best Solution in previous 3 generations =",
                                              ','.join([str(i)
                                                        for i in best_generation['solution']])]),
                                    ' '.join(["Worst Fitness in previous 3 generations =",
                                              str(worst_generation['fitness'])]),
                                    ' '.join(["Worst Solution in previous 3 generations =",
                                              ','.join([str(i)
                                                        for i in worst_generation['solution']])]),
                                    ' '.join(["Best Average Fitness in previous 3 generations:",
                                              str(best_average)]),
                                    ' '.join(["Worst Average Fitness in previous 3 generations:",
                                              str(worst_average)]),
                                ]
                                print('\n'.join(failure_array))
                                print(FAILED)
                            else:
                                self.failures_remaining -= 1
                                print("Failed")
                                fail_message = FAILURES_REMAINING_MSG + f"{self.failures_remaining}"
                                print(fail_message)
                        else:
                            continue
        return needs_termination

    def save_generation_data_bisection(self):
        """
        Saves the current generation data for bisection and checks for termination conditions.
        
        Returns:
            bool: True if the run needs to be terminated, False otherwise.
        """
        needs_termination = False
        self.get_generation_data()
        # Create a message summarizing the current generation's fitness
        message_array = [f"Generation {self.generation_number}: ",
                         f"(B: {self.generation_data['best']['fitness']},",
                         f"A: {self.generation_data['average']},",
                         f"W: {self.generation_data['worst']['fitness']})"]
        message = ' '.join(message_array)
        self.generation_data['message'] = message
        print(message)
        # Print detailed debug information if enabled
        if self.full_debug or self.limited_debug:
            debug_array = [
                "Current Population",
                '\n'.join([i.solution_as_string()
                           for i in self.population.current_generation]),
                ' '.join(["Best Solution =",
                          (','.join([str(i)
                           for i in self.generation_data['best']['solution']]))]),
                ' '.join(["Worst Solution =",
                          (','.join([str(i)
                           for i in self.generation_data['worst']['solution']])), '\n'])
            ]
            print('\n'.join(debug_array))
        self.saved_generation_data.append(self.generation_data)

        # Check if the best fitness matches the string size, indicating success
        if self.string_size == self.generation_data['best']['fitness']:
            success_array = [
                ' '.join(["Global Best Fitness =",
                          str(self.generation_data['best']['fitness'])]),
                ' '.join(["Global Best Solution =",
                          ','.join([str(i)
                                    for i in self.generation_data['best']['solution']])]),
                ' '.join(["Global Best was at index",
                          str(self.generation_data['best']['index']),
                          "of",
                          str(len(self.population.current_generation))]),
                ' '.join(["Average Fitness:",
                          str(self.generation_data['average'])]),
                ' '.join(["Worst Fitness:",
                          str(self.generation_data['worst']['fitness'])]),
            ]
            print('\n'.join(success_array))
            print(SUCCESS)
            needs_termination = True

        # Maintain a sliding window of the last 4 generations
        if len(self.saved_generation_data) == 4:
            self.saved_generation_data.pop(0)
        return needs_termination

    def run(self):
        """
        Runs the genetic algorithm based on the settings. Handles both standard and bisection options.
        """
        print(json.dumps(sl.ga_settings, indent=4))
        terminate_run = False
        print("bisection_option: ", self.bisection_option)
        if self.bisection_option == 0:
            # Standard genetic algorithm run
            self.population.initialize_random_starting_population()
            terminate_run = self.save_generation_data()
            self.generation_number += 1
            while True:
                self.population.select_mating_parents()
                self.population.replace_current_population()
                terminate_run = self.save_generation_data()
                if terminate_run:
                    break
                self.generation_number += 1
        elif self.bisection_option == 1:
            # Bisection method for finding optimal population size
            while True:
                sl.set_setting(POPULATION_SIZE_N,
                               self.bisection_starting_population)
                print("\nRunning bisection with population size: " +
                      str(self.bisection_starting_population))
                self.population.initialize_random_starting_population()
                terminate_run = self.save_generation_data_bisection()
                self.generation_number += 1
                while True:
                    self.population.select_mating_parents()
                    self.population.replace_current_population()
                    terminate_run = self.save_generation_data_bisection()
                    if self.generation_number >= self.bisection_max_generation:
                        self.bisection_starting_population *= 2
                        break
                    if terminate_run:
                        break
                    self.generation_number += 1
                if terminate_run:
                    print(f"Max N = {self.bisection_starting_population}")
                    print(f"Min N = {self.bisection_starting_population//2}")
                    self.bisection_min = self.bisection_starting_population // 2
                    self.bisection_max = self.bisection_starting_population
                    self.bisection_starting_population = (
                        (self.bisection_max + self.bisection_min) // 2)
                    self.generation_number = 1
                    break
                self.generation_number = 1

            while True:
                sl.set_setting(POPULATION_SIZE_N,
                               self.bisection_starting_population)
                print("\nRunning bisection with population size: " +
                      str(self.bisection_starting_population))
                self.population.initialize_random_starting_population()
                terminate_run = self.save_generation_data_bisection()
                self.generation_number += 1
                while True:
                    self.population.select_mating_parents()
                    self.population.replace_current_population()
                    terminate_run = self.save_generation_data_bisection()
                    if self.generation_number >= self.bisection_max_generation:
                        self.bisection_min = self.bisection_starting_population
                        self.bisection_starting_population = (
                            (self.bisection_max + self.bisection_min) // 2)
                        break
                    if terminate_run:
                        break
                    self.generation_number += 1
                if terminate_run:
                    print(f"Max N = {self.bisection_starting_population}")
                    print(f"Min N = {self.bisection_min}")
                    self.bisection_max = self.bisection_starting_population
                    self.bisection_starting_population = (
                        (self.bisection_max + self.bisection_min) // 2)
                    self.generation_number = 1
                if (((((self.bisection_max - self.bisection_min) /
                        self.bisection_min)) < self.bisection_threshold) or
                        self.bisection_max - self.bisection_min == 1):
                    print(f"Final Max N = {self.bisection_max}")
                    print(f"Final Min N = {self.bisection_min}")
                    final_threshold = ((self.bisection_max - self.bisection_min) /
                                       self.bisection_min)
                    print(f"Final Threshold = {final_threshold}")
                    break
                self.generation_number = 1


if __name__ == "__main__":
    """
    Main entry point for the script. Loads settings, initializes the controller, and runs the algorithm.
    """
    start = time.time()
    sl.load_settings(sys.argv)
    sga_controller = SGAController()
    sga_controller.run()
    end = time.time()
    print(f"Execution time: {end-start} seconds")

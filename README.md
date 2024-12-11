
# Simple Genetic Algorithm Enhanced

## License
This project is licensed under the [Unlicense](http://unlicense.org/).

## Project Description
Simple Genetic Algorithm Enhanced (SGA-Enhanced) is an extension of a basic genetic algorithm (GA) implementation. The project introduces new functionalities to improve the flexibility and performance of genetic algorithms. These enhancements include new crossover operators, a bisection mode for optimizing population size, and a trap-4 fitness function. The algorithm is designed to solve binary string optimization problems and is capable of identifying the optimal parameters for diverse scenarios.

### Key Features
- **New Crossover Operators**: One-point and two-point crossovers.
- **Trap-4 Fitness Function**: A nuanced fitness evaluation strategy.
- **Bisection Mode**: Automates the determination of the minimum population size required for a problem.
- **Debugging Options**: Limited and full debugging modes for enhanced traceability.

## Crossover Operators
The project supports three crossover operators:
1. **Uniform Crossover** (Default): Each bit in the offspring is selected randomly from one of the parents.
2. **One-Point Crossover**: A single crossover point is selected; parts before and after the point are swapped between parents to create offspring.
3. **Two-Point Crossover**: Two crossover points are chosen, and the segments between these points are swapped.

### Impact on Results
- One-point crossover performs best for shorter string sizes.
- Two-point crossover is optimal for larger strings, as it introduces more genetic diversity.
- Uniform crossover performs poorly for the trap-4 function due to limited directed diversity.

## Trap-4 Fitness Function
This fitness function evaluates the binary string by dividing it into partitions of four bits. Each partition’s fitness depends on the number of 1s it contains:
- **0 1’s**: Fitness = 3
- **1 1’s**: Fitness = 2
- **2 1’s**: Fitness = 1
- **3 1’s**: Fitness = 0
- **4 1’s**: Fitness = 4

The overall fitness is the sum of the partition fitness values. This function provides a challenging optimization landscape, with the global optimum being a string of all 1s.

## Bisection Mode
Bisection mode identifies the minimum population size required to solve a problem within a defined number of generations. It doubles the population size until success is achieved, then narrows the range to pinpoint the minimum viable size.

### Parameters
- `bisectionThreshold`: Defines the acceptable range for population size optimization.
- `bisectionStartingPopulation`: Initial population size for the bisection process.
- `bisectionMaxGeneration`: Maximum number of generations for each bisection step.

## Settings and Debugging
- `fitnessFunction`: Specifies the fitness function (0 = one-max, 1 = trap-4).
- `crossoverOperator`: Defines the crossover operator (0 = uniform, 1 = one-point, 2 = two-point).
- `probApplyCrossover`: Probability of applying crossover to a pair of parents.
- `probApplyMutation`: Probability of mutating an individual.
- Debugging can be toggled using `-g` (limited) or `-G` (full).

## Results
### Summary of Experiments
The experiments tested all combinations of crossover operators and fitness functions across varying string sizes (24, 48, 100). Key findings:
- **Uniform Crossover**: Only succeeded for a string size of 24 with low crossover probability (0.2).
- **One-Point Crossover**: Best for string size 24; slower for larger sizes.
- **Two-Point Crossover**: Most efficient for string sizes 48 and 100.

### Performance Metrics
| Crossover Operator | String Size | Min N | Max N | Threshold | Execution Time (s) |
|---------------------|-------------|-------|-------|-----------|--------------------|
| Uniform             | 24          | 75    | 80    | 0.06667   | 0.98675            |
| One-Point           | 24          | 65    | 70    | 0.07692   | 0.57457            |
| Two-Point           | 24          | 120   | 130   | 0.08333   | 0.95921            |
| One-Point           | 48          | 320   | 340   | 0.06250   | 10.89071           |
| Two-Point           | 48          | 150   | 160   | 0.06667   | 3.84175            |
| One-Point           | 100         | 1440  | 1520  | 0.05556   | 109.20490          |
| Two-Point           | 100         | 1280  | 1360  | 0.06250   | 87.42322           |

## Conclusion
- **Uniform Crossover**: Not suitable for trap-4 optimization.
- **One-Point Crossover**: Ideal for smaller string sizes.
- **Two-Point Crossover**: Superior for larger strings, balancing diversity and convergence speed.

## How to Run
Use the following command to execute the program:
```bash
python3 sga.py [-h] [-g] [-G] [settings file]
```
- **Bisection Mode**: Set `bisection` to `1` in the settings file.
- Default settings file: `gasettings.dat`.

Refer to the documentation for additional configuration options.

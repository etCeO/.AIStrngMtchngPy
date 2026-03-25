# Evolutionary String Matching Optimization
### String Matching Using Genetic Algorithms

- A python program that uses genetic algorithms to evolve a population of random strings into a given target string by repeatedly applying methods of selection, crossover, and mutation.

## Author Info

- Full Name: Ethan E. Lopez
- Chapman Email: etlopez@chapman.edu

## Usage

Run the program command line:

python project2.py

No arguments required. The parameters (population size, mutation rate, etc.) are set inside the script and can be easily adjusted with user preference.

## Input Format

This program doesn't require additional input files.

### Target String

- Fixed Target String:

Hello CPSC 390!

- Length of String: 15 characters (including space and punctuation)

### Character Set

- Characters are chosen from printable ASCII characters.
- Range of Character Set:
space (' ') ASCII code 32 to z ASCII code 122.
- Total Possible Values per Character: 91

### Initial Population

- Population Size: 128
- Each Individual of Population:

A string of length 15

- Randomly generated with uniform probability over the possible set of characters.

## Output

During Execution:

1. Every 10 generations
2. Generation Number
3. Best Individual in the population
4. Fitness Score (0-15)

Example:

- Generation 100: Best = "Hella CPSB 390!" | Fitness = 13  

Final Output:  

1. Final best string  
2. Final fitness score  
3. Total number of generations  
4. Fitness Plot: 

- Plot is generated using matplotlib  
- Shows the X-axis (in log scale): generation number  
- Shows the Y-axis (in linear scale): best fitness scores

## Implementation Details

**Genetic Algorithm Components**

1. Fitness Function

- Measures the similarity to the target string
- Defined as:
The number of characters that match the target string at the corresponding positions
- Maximum fitness: 15
  
2. Selection

- Selects the parents for the genetic algorithm
- The fitness of the individual is directly proportional to the selection probability
- Roulette wheel selection is the most common selection method

3. Crossover

- Combines the two parents to form offspring
- Probability of crossover:
Applied to the parents
- The most common method of crossover is:
Single-point crossover
- Parents are divided at random points, and the substrings are swapped to form offspring

4. Mutation

- Random changes are introduced to the offspring
- Mutation rate:
~0.05 per character
- For each character, the mutation operation is as follows:

Probability p, random ASCII character
   
**Algorithm Flow**

1. Randomly generate the initial population
2. Evaluate the fitness of the individuals
3. Until termination criteria are met

   Select parents
   Apply crossover
   Apply mutation
   Create the next generation
   Keep track of the best individual
   Print the results and plot the fitness
   
**Stopping Criteria**

1. A perfect match has been achieved
   "Hello CPSC 390!"
2. Maximum number of generations has been reached
   5000 iterations

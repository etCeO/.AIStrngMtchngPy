"""
Ethan E. Lopez
March 5, 2026
Project 2: String Matching Using Genetic Algorithm

References
Canvas Materials
  1. 03_local-search_slides.pdf
  2. Homework 4
  3. Previous CPSC 392 (Intro to Data Science) Projects
        a. Strictly for reviewing how to modify matplotlib parameters and visuals
AI Platforms
  1. CHATGPT
  2. GITHUB COPILOT
      - you'll see comments throughout this code where all AI tools were implemented

README
this script uses genetic algorithms to produce offsoring that generate the target string

BRAINSTORMING

Specifications

1. String Representations
  - Each individual is a string of exactly 15 chars
  - Each character is drawn from the printable ASCII range
      - '' to 'z' (32 to 122 in ASCII) --> 91 possible values
  - the initial population is random

2. Population
    - size = 128
    - constant across all generations

3. Stopping criteria
    - algorithm terminates when a perfect match is found or the max generation limit of 5000 is reached

Core Complements
+ Fitness Function
+ Selection of parents
+ Crossover to produce offspring

Crossover Rate
    - generate a random probability

Mutation
    - decide whether to mutate a character based on probability

REQUIRED OUTPUT
- print the generation number
- best fitness score is 15
- desired string  --> "Hello CPSC 390!"

Ex.
Gen    0 | Fitness: 3/15 | Best: "Jdlksjie8932"
Gen   10 | Fitness: 5/15 | Best: "Hdllo CPSv +90!"
Gen   20 | Fitness: 8/15 | Best: "Hello CZNP 390!"
...
Gen 5000 | Fitness: 15/15 | Best: "Hello CPSC 390!"

Fitness Plot
+ draw a single plot showing how best fitness improves
    Axes:
    - x-axis: generation number
    - y-axis: best fitness score (0 to 15)
+ plot at every generation
+ label both axes with a descriptive title
+ use matplotlib to create the plot (plt.xscale('log') for better visualization)

"""
import random # imports random number generator
import matplotlib.pyplot as plt # imports matplotlib for fitness plot

def cross_over(p1, p2, c_rate):
# a function that performs the crossover between two parents
    # includes 3 parameters
    # 1) p1: parent 1
    # 2) p2: parent 2
    # 3) cross_rate: the crossover rate or the probability of actually performing crossover
    
    r = random.random() # generate a random number between 0 and 1
    # this value determines if the crossover happens or not
    c_point = random.randint(1,14) # select a random number for the crossover point (between 1 and 14)
    # this value determines after which point the crossover will occur

    if r < c_rate: # if the random number is less than the crossover rate
        # produce two children (the offspring of parents 1 and 2)
        child1 = p1[:c_point] + p2[c_point:] # child 1 gets the first c_point chars from p1 and the last (1-c_point) chars from p2
        child2 = p2[:c_point] + p1[c_point:] # child 2 gets the first c_point chars from p2 and the last (1-c_point) chars from p1
        children = [child1, child2] # add the two children to the list
        return children # return the two children
    else: # otherwise we skip the crossover
        return [p1, p2] # simply return parents 1 and 2 because they are the copies of the parents

def mutate(children, m_rate):
# a function for randomly mutating offspring by changing characters
# children is a list of child strings (after cross_over function)
# m_rate is the predefined mutation rate boundary (0.05)
    offspring = [] # initialize an empty list for the new offspring
    for child in children: # for each child in the list of children
        offspr = "" # initialize an empty string for a mutated child
        for char in child: # for each character in the child string
            r = random.random() # generate a random number between 0 and 1
            if r < m_rate: # if the random number is less than the mutation rate, mutate the character
                m_char = chr(random.randint(32, 122)) # randomly select from the printable ASCII range 
                offspr += m_char # add the mutated character to the mutated offspring string
            else: # otherwise simply add the original character (no mutation occurs)
                offspr += char 
        offspring.append(offspr) # add the mutated (or unmutated) child to the offspring list
    return offspring # return the list of mutated children (final offspring)

def get_fitness(strng, target):
# a function for calculating the fitness score of a single string
# compares strings to the goal in the population
# strng is the string being analyzed
# target is the target string ("Hello CPSC 390!")
    f_score = 0 # initialize score to 0
    idx = 0 # initialize index to 0 for iterating through the string
    for char in strng: # for each character in the string
        if idx < len(target): # if the index is within the bounds of the target string
            if char == target[idx]: # if the character matches the corresponding character in the target string
                f_score += 1 # we increase fitness score by 1
        idx += 1 # increment index by 1 to move to the next character
    return f_score # return the final fitness score

def create_population():
# a function for creating the population of 128 random strings (16 chars)
    population = {} # in this program, the population is an empty dictionary
    i = 0 # count of individuals
    while i < 128: # for all 128 random individuals

        # OLD METHOD
        # indv = "" # initialize an empty string for the individual
        # for _ in range(15): # for each character in the string (15 chars total)
        #     indv += chr(random.randint(32, 122)) # add a random character from the printable ASCII range to the individual string

        # CHATGPT ASSISTANCE
        # to improve efficiency and simplify previous code
        # prompt: "how do you modify this for better efficiency? : indv = "" # initialize an empty string for the individual
        # for _ in range(15): # for each character in the string (15 chars total)
        #     indv += chr(random.randint(32, 122)) # add a random character from the printable ASCII range to the individual string?"
        indv = ''.join(chr(random.randint(32, 122)) for _ in range(15)) 
        # get a random character from the ascii range and join all chars together to create a random string of 15

        population[indv] = 0 # add the individual to the population dictionary
        i += 1 # increment individual count by 1
    return population # return the initial population

def get_parents(population):
# defines a function for selecting parents from the population
# uses the Roulette Wheel method taught in class
# mirrors real life, where even weaker individuals can reproduce
# stronger individuals, however, have a better chance

    fitness_scores = population.values() # get the fitness scores of all individuals
    individuals = list(population.keys()) # get the list of individuals from the population dictionary

    # REGULAR METHOD
    total_fitness = sum(fitness_scores) # calculate total fitness scores of the population
    probs = [population[indv] / total_fitness for indv in population] # calculate the probability for each individual based on their fitness scores
    
    # GITHUB COPILOT ASSISTANCE
    # for creating accurate parameters in the random choice() function
    # prompt: 
    # "how do you use random.choices() to select 2 parents from a list of individuals based on their fitness scores as weights?"
    parents = random.choices(individuals, weights=probs, k=2) # randomly select 2 parents based on probabilities
    # i recognize from this that there is a small chance an individual reproduces from itself
    # however, i think this allowable for the genetic algorithm not only in terms of mirroring cell self-reproduction, but also allowing strong individuals to dominate from time to time
    # mutations also support additional string diversity made during each sequence generation, so this prevents exact copies from replicating too much

    p1 = parents[0] # first select parent 1
    p2 = parents[1] # then select parent 2


    # # EXTRA CREDIT 1
    # # squaring fitness scores to leverage larger weights during parent selection
    # squared_scores = [score ** 2 for score in fitness_scores] # square the fitness scores to increase the selection probabilities on stronger individuals (decrease for weaker individuals)
    # total_fitness = sum(squared_scores) # calculate total fitness scores of the population using the squared scores for probability calculation
    # probs = [sq_score / total_fitness for sq_score in squared_scores] # calculate the probability for each individual based on their squared fitness scores
    # parents = random.choices(individuals, weights=probs, k=2) # randomly select 2 parents based on probabilities
    # p1 = parents[0] # first select parent 1
    # p2 = parents[1] # then select parent 2
    
    # # EXTRA CREDIT 2/2.5 (this code is for both algorithms 2 and 2.5)
    # # (when running either one, always be sure this section is uncommented)
    # rank_count = 0 # initialize a variable to count the rank number
    # rank1 = [indv for indv in individuals if population[indv] == 1] # rank individuals with fitness score 1
    # rank2 = [indv for indv in individuals if population[indv] == 2] # rank individuals with fitness score 2
    # rank3 = [indv for indv in individuals if population[indv] == 3] # rank individuals with fitness score 3
    # rank4 = [indv for indv in individuals if population[indv] == 4] # rank individuals with fitness score 4
    # rank5 = [indv for indv in individuals if population[indv] == 5] # rank individuals with fitness score 5
    # rank6 = [indv for indv in individuals if population[indv] == 6] # rank individuals with fitness score 6
    # rank7 = [indv for indv in individuals if population[indv] == 7] # rank individuals with fitness score 7
    # rank8 = [indv for indv in individuals if population[indv] == 8] # rank individuals with fitness score 8
    # rank9 = [indv for indv in individuals if population[indv] == 9] # rank individuals with fitness score 9
    # rank10 = [indv for indv in individuals if population[indv] == 10] # rank individuals with fitness score 10
    # rank11 = [indv for indv in individuals if population[indv] == 11] # rank individuals with fitness score 11
    # rank12 = [indv for indv in individuals if population[indv] == 12] # rank individuals with fitness score 12
    # rank13 = [indv for indv in individuals if population[indv] == 13] # rank individuals with fitness score 13
    # rank14 = [indv for indv in individuals if population[indv] == 14] # rank individuals with fitness score 14
    # ranks = [rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9, rank10, rank11, rank12, rank13, rank14] # create ranks list from defined ranks
    # probs = [] # list of probabilities for each rank

    # EXTRA CREDIT 2
    # total_fitness = sum(fitness_scores) # calculate total fitness scores of the population
    # i = 1 # set counter for rank number
    # for rank in ranks: # for every rank in the ranks list
    #     if len(rank) > 0: # if the list is not empty
    #         rank_count += 1 # increment rank count by 1 
    #         rank_fitness = i * len(rank) # calculate total fitness of the rank by multiplying the fitness score by total individuals in each list
    #         prob_rank = rank_fitness / total_fitness # this rank's probability is the rank's fitness divided by the total fitness
    #         probs.append(prob_rank) # append rank probability to the probabilities list
    #     else: # if the list is empty
    #         probs.append(0.0) # probability is 0
    #     i += 1 # increment rank counter
    # parent_ranks = random.choices(ranks, weights=probs, k=2) # randomly select 2 ranks based on probabilities
    # p1 = random.choice(parent_ranks[0]) # randomly select parent 1 from the first selected rank
    # p2 = random.choice(parent_ranks[1]) # randomly select parent 2 from the second selected rank

    # # EXTRA CREDIT 2.5   
    # for rank in ranks: # for every rank in the ranks list
    #     if len(rank) > 0: # if the list is not empty
    #         rank_count += 1 # increment rank count by 1 
    # if rank_count > 3: # if the rank count is greater than 3, this is where we distinguish between weak and strong individuals
    #     # large, strong probabilities go towards the 3 biggest ranks/individual lists
    #     # small, weak probabilities go towards the remaining ranks/individuals
    #     r = rank_count - 1 # calculate how times we should add the denominator to get the small probability
    #     # (if we had 6 ranks, this would be 5)
    #     x = r*2 # set denominator as r times 2 (5x2 = 10)
    #     small_prob = 1/x # calculate weak probabilities (1/10 = 0.1)
    #     small_sections = rank_count - 3 # determine how many sections are going to be weak probabilities (all except top 3 ranks)
    #     # (ex. 6-3 = 3 weak sections of 0.1)
    #     big_prob = (1 - (small_prob*small_sections)) / 3 # calculate the value of strong probabilities
    #     # this is 1 minus the number of small sections times probability divided by 3 since it's only the top 3 that have strong probabilities
    #     # (ex. 1 - (3*0.1) / 3 = 0.23, meaning ranks 4, 5, and 6 would have a probability of 0.23)
    # i = 1 # set a counter for looping through existing ranks only
    # for rank in ranks: # for all ranks in the rank list
    #     if rank_count < 4: # if the rank count is smaller than 4
    #         prob = 1/rank_count # we assign equal probabilities
    #         if len(rank) > 0: # if there's a rank that has individuals
    #             probs.append(prob) # assign this equal probability to it
    #         else: # otherwise empty
    #             probs.append(0.0) # assign 0 
    #     else: # if the rank count is 4 or more
    #         if len(rank) > 0: # if there's a rank with individuals
    #             if i <= small_sections: # if this is a weak rank (i = 1 means this is the lowest existing rank)
    #                 probs.append(small_prob) # assign this to the small probability
    #             else: # otherwise
    #                 probs.append(big_prob) # assign this to the large probability
    #             i += 1 # increment existing ranks count
    #         else: # otherwise empty
    #             probs.append(0.0) # assign 0
    # parent_ranks = random.choices(ranks, weights=probs, k=2) # randomly select 2 ranks based on probabilities
    # p1 = random.choice(parent_ranks[0]) # randomly select parent 1 from the first selected rank
    # p2 = random.choice(parent_ranks[1]) # randomly select parent 2 from the second selected rank


    return p1, p2 # return the selected parents

def build_fitness_plot(best_scores):
# a function for building the fitness plot using matplotlib
    
    # here is where I referred back to previous CPSC 392 projects to review how to modify matplotlib parameters and visuals for a more polished plot
    plt.figure(figsize=(10, 6)) # set the figure size
    plt.plot(best_scores, linewidth=2, marker='o', markersize=3, label='Best Fitness') # plot the fitness scores with markers and lines
    plt.xscale('log') # set x-axis to logarithmic scale
    plt.xlabel('Generation', fontsize=12) # label x-axis
    plt.ylabel('Best Fitness Score', fontsize=12) # label y-axis
    plt.title('Best Fitness Over Generations', fontsize=14) # set title of the plot
    plt.grid(True, linestyle='', alpha=0.6) # add grid for better readability
    plt.show() # display the plot
    
# MAIN CODE
print() # newline for neatness

# KEY INSTANCES
target = "Hello CPSC 390!" # target string
cross_rate = 0.82 # crossover rate
mutate_rate = 0.05 # mutation rate
gen = 0 # counts generations
perfect_match = False # a boolean to check whether we found the perfect match or not

# PROGRAM OPERATIONS

# initialize population of 128 random strings
population = create_population() # this function produces 128 strings in a list
best_scores = [] # create an empty list for storing the best fitness scores

# evaulate fitness of every individual
for indv in population: # for all individuals in the population
    population[indv] = get_fitness(indv, target) # calculate the fitness score and store it in the score list
best_fitness = max(population.values()) # find the best fitness score in the initial population
best_scores.append(best_fitness) # add the best fitness score to the list of best scores for plotting
best_individual = max(population, key=population.get) # find the individual with the best fitness score
if best_fitness == 15: # if we find a perfect match (fitness score of 15)
    perfect_match = True # set the perfect match boolean to true

# while no perfect match found and generation is less than the maximum number of iterations
while (perfect_match == False) and (gen < 5000):
    if gen % 10 == 0: # if the generation number is a multiple of 10

        # GITHUB COPILOT ASSISTANCE
        # for formatting the print statement to show the correct information in the correct format
        # before this, I didn't know how to print out the double quotes surrounding the best individual using tabs
        # prompt: "how do i modify this print statement to get double quotes around Best (e.g. Best: "Hello CPSC 390!") : print(f"Gen {gen:5d} | Fitness: {best_fitness}/15 | Best: ''{best_individual}''")
        print(f"Gen {gen:5d} | Fitness: {best_fitness}/15 | Best: \"{best_individual}\"") # print the gen number, fitness score, and individual

    new_population = {} # initialize an empty dictionary for the new population
    for i in range(64): # we need to create 64 pairs of parents (128 individuals total)
        p1, p2 = get_parents(population) # select two parents from the population based on fitness scores
        children = cross_over(p1, p2, cross_rate) # perform crossover to produce offspring
        offspring = mutate(children, mutate_rate) # perform mutation on the offspring
        for child in offspring: # for each child in the list of offspring
            new_population[child] = get_fitness(child, target) # calculate the fitness score of the child and add it to the new population dictionary
    population = new_population # replace the old population with the new population
    best_fitness = max(population.values()) # find the best fitness score in the initial population
    best_scores.append(best_fitness) # add the best fitness score to the list of best scores for plotting
    best_individual = max(population, key=population.get) # find the individual with the best fitness score
    if best_fitness == 15: # if we find a perfect match (fitness score of 15)
        perfect_match = True # set the perfect match boolean to true
    gen += 1 # increment generation number by 1

print(f"Gen {gen:5d} | Fitness: {best_fitness}/15 | Best: \"{best_individual}\"") # print the gen number, fitness score, and individual of the final generation
print() # newline for neatness

if best_individual == target: # if the best individual reached the target string
    print(f"Solution found in generation {gen}!") # print the generation number where the solution was found
else: # otherwise
    print("No solution found within the generation limit.") # say there was no solution found

print() # newline for neatness

build_fitness_plot(best_scores) # call the function to build the fitness plot using the list of best scores
print() # newline for neatness






# # TESTING CODE
# # + AI Verification Methods

# target = "Hello CPSC 390!" # target string for testing

# # TESTING CREATE_POPULATION FUNCTION
# population = {} # in this program, the population is an empty dictionary

# # OR TO SEE THE FIRST HALF OF THE WRITTEN EXAMPLE (fitness scores and probabilities)
# # population = {'lr-w"l(,9p a*a)': 0, "$htYUbne'v[3aVJ": 0, '\\dZIW?4-IQmjN]]': 0, '^p#J!YQ`,5VvYp^': 0, 'OC"d\'\'np3FC0i<>': 0, 'a?tynL@O&oGnHQ0': 0, '*eJX)92VW(m$g)Y': 0, 'Xj<15i?eG0"@:GC': 0, 'Jdn9[ktB\\vV%on+': 0, 'nh%*g%!j?hau%Kr': 0}
# # when testing this, comment out line 259 and lines 265-277

# i = 0 # count of individuals
# while i < 20: # for all _ random individuals

#      # CHATGPT ASSISTANCE
#      # to improve efficiency and simplify previous code
#      # prompt: "how do you modify this for better efficiency? : indv = "" # initialize an empty string for the individual
#      # for _ in range(15): # for each character in the string (15 chars total)
#      #     indv += chr(random.randint(32, 122)) # add a random character from the printable ASCII range to the individual string?"
#      indv = ''.join(chr(random.randint(32, 122)) for _ in range(15)) 
#      # get a random character from the ascii range and join all chars together to create a random string of 15

#      population[indv] = 0 # add the individual to the population dictionary
#      i += 1 # increment individual count by 1
# print(population) # return the initial population

# print()
# # TESTING GET_FITNESS FUNCTION
# for indv in population: # for all individuals in the population
#     population[indv] = get_fitness(indv, target) # calculate the fitness score and store it in the score list
# print(population) # return the population with fitness scores

# print()
# # TESTING GET_PARENTS FUNCTION
# fitness_scores = population.values() # get the fitness scores of all individuals
# print(fitness_scores) # print the fitness scores for testing
# individuals = list(population.keys()) # get the list of individuals from the population dictionary
# total_fitness = sum(fitness_scores) # calculate total fitness scores of the population
# print(total_fitness) # print the total fitness for testing
# probs = [population[indv] / total_fitness for indv in population] # calculate the probability for each individual based on their fitness scores
# print(probs) # print the probabilities for testing

#     # GITHUB COPILOT ASSISTANCE
#     # for creating accurate parameters in the random choice() function
#     # prompt: 
#     # "how do you use random.choices() to select 2 parents from a list of individuals based on their fitness scores as weights?"
# parents = random.choices(individuals, weights=probs, k=2) # randomly select 2 parents based on probabilities

# parent1 = parents[0] # first select parent 1
# parent2 = parents[1] # then select parent 2
# print(parent1, parent2) # return the selected parents

# print()
# # TESTING CROSSOVER FUNCTION
# print("Testing cross_over function:")
# r = random.random() # generate a random number between 0 and 1
# c_point = random.randint(1,14) # select a random number for the crossover point (between 1 and 14)
# print(f"Random number for crossover: {r:.4f}, Crossover point: {c_point}") # print the random number and crossover point for testing
# if r < 0.82: # if the random number is less than the crossover rate
#     print("Performing crossover...") # indicate that crossover will occur
#     child1 = parent1[:c_point] + parent2[c_point:] # child 1 gets the first c_point chars from p1 and the last (1-c_point) chars from p2
#     child2 = parent2[:c_point] + parent1[c_point:] # child 2 gets the first c_point chars from p2 and the last (1-c_point) chars from p1
#     children = [child1, child2] # add the two children to the list
#     print(children) # return the two children
# else: # otherwise we skip the crossover
#     print("Skipping crossover...")
#     children = [parent1, parent2]
#     print(children)

# # TESTING MUTATE FUNCTION
# offspring = [] # initialize an empty list for the new offspring
# for child in children: # for each child in the list of children
#     print()
#     print(f"Testing mutate function on child: {child}") # print the child being tested
#     offspr = "" # initialize an empty string for a mutated child
#     for char in child: # for each character in the child string
#         r = random.random() # generate a random number between 0 and 1
#         print(f"Random number for mutation: {r:.4f}")
#         if r < 0.05: # if the random number is less than the mutation rate, mutate the character
#             print("Mutating character...")
#             m_char = chr(random.randint(32, 122)) # randomly select from the printable ASCII range
#             print(f"Original char: '{char}', Mutated char: '{m_char}'") # print the original and mutated character for testing
#             offspr += m_char # add the mutated character to the mutated offspring string
#         else: # otherwise simply add the original character (no mutation occurs)
#             print("No mutation for character: '{char}'") # indicate that no mutation occurred for this character
#             offspr += char 
#     offspring.append(offspr) # add the mutated (or unmutated) child to the offspring list
# print(offspring) # return the list of mutated children (final offspring)
# print()


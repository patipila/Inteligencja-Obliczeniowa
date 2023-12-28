import numpy as np
import random
import matplotlib.pyplot as plt

# Function to calculate the total distance of a tour
def calculate_distance(tour, distances):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distances[tour[i], tour[i + 1]]
    total_distance += distances[tour[-1], tour[0]]  # Return to the starting city
    return total_distance

# Function to generate an initial population of tours
def generate_population(size, num_cities):
    population = []
    for _ in range(size):
        tour = list(range(num_cities))
        random.shuffle(tour)
        population.append(tour)
    return population

# Tournament selection
def tournament_selection(population, distances):
    tournament_size = 5
    tournament = random.sample(population, tournament_size)
    best_tour = min(tournament, key=lambda x: calculate_distance(x, distances))
    return best_tour

# Order crossover (OX) operator
def order_crossover(parent1, parent2):
    start = random.randint(0, len(parent1) - 1)
    end = random.randint(start + 1, len(parent1))
    child = [-1] * len(parent1)

    # Copy the segment from parent1 to the child
    child[start:end] = parent1[start:end]

    # Fill in the remaining positions from parent2
    index = end
    for city in parent2 + parent2:
        if city not in child:
            child[index % len(parent1)] = city
            index += 1
        if index % len(parent1) == start:
            break

    return child

# Mutation: Swap two cities in the tour
def mutate(tour):
    index1, index2 = random.sample(range(len(tour)), 2)
    tour[index1], tour[index2] = tour[index2], tour[index1]
    return tour

# Genetic Algorithm for TSP
def genetic_algorithm(num_cities, distances, population_size, generations):
    population = generate_population(population_size, num_cities)

    for generation in range(generations):
        # Select parents using tournament selection
        parents = [tournament_selection(population, distances) for _ in range(population_size)]

        # Create offspring using crossover
        offspring = []
        for i in range(0, population_size, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child1 = order_crossover(parent1, parent2)
            child2 = order_crossover(parent2, parent1)
            offspring.extend([child1, child2])

        # Apply mutation to the offspring
        offspring = [mutate(child) for child in offspring]

        # Select the best individuals for the next generation
        population = sorted(population + offspring, key=lambda x: calculate_distance(x, distances))[:population_size]

        # Print the best distance in each generation
        best_distance = calculate_distance(population[0], distances)
        print(f"Generation {generation + 1}, Best Distance: {best_distance}")

    # Return the best tour and its distance
    best_tour = population[0]
    return best_tour, calculate_distance(best_tour, distances)

# Example usage:
# Specify the number of cities and the distance matrix
num_cities = 10
distances = np.random.rand(num_cities, num_cities)
distances = distances + distances.T  # Make the matrix symmetric

# Set algorithm parameters
population_size = 50
generations = 1000

# Run the genetic algorithm
best_tour, best_distance = genetic_algorithm(num_cities, distances, population_size, generations)

print(f"Best Tour: {best_tour}")
print(f"Best Distance: {best_distance}")

# Plot the best tour
plt.figure()
plt.plot(distances[:, 0], distances[:, 1], 'o')
plt.plot(distances[best_tour, 0], distances[best_tour, 1], 'r-')
plt.title("Best Tour")
plt.show()
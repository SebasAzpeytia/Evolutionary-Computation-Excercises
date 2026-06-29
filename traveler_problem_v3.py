import pandas as pd
import random
import copy
from itertools import pairwise


class DNA:
    def __init__(self, map_df, start_node="A"):
        self.map_df = map_df
        self.start_node = start_node

        self.route = self.initialize_route()
        self.distance = self.calculate_distance()
        self.fitness = 1 / self.distance

    def initialize_route(self):
        # Pasos 1 y 2. Generamos la lista de ciudades y eliminamos la ciudad inicial.
        intermediate_cities = list(self.map_df.columns.drop(self.start_node))

        # Paso 3. Revolvemos la lista obtenida.
        random.shuffle(intermediate_cities)

        # Paso 4. Agregamos las ciudades faltantes concatenandolas.
        return [self.start_node] + intermediate_cities + [self.start_node]

    def calculate_distance(self):
        total_distance = 0

        for current_city, next_city in pairwise(self.route):
            distance_between = self.map_df.at[current_city, next_city]

            total_distance += distance_between

        return total_distance

    # Mutate by swapping two genes (cities) in the route
    def mutate(self, probability=0.1):
        if random.random() < probability:
            # Seleccionar el indice de dos nodos aleatoriamente
            mutable_nodes = range(1, len(self.route) - 1)
            n1, n2 = random.sample(mutable_nodes, 2)

            # Intercambiamos ambos nodos
            self.route[n1], self.route[n2] = self.route[n2], self.route[n1]

            # Recalculamos la distancia y aptitud nuevas
            self.distance = self.calculate_distance()
            self.fitness = 1 / self.distance


class Population:
    def __init__(self, map_df, size=100, start_node="A"):
        self.map_df = map_df
        self.size = size
        self.population = [DNA(map_df, start_node) for _ in range(size)]
        self.best_individual = None

    def evolve(self):
        # Extract fitness for weighted selection
        fitnessList = [ind.fitness for ind in self.population]

        new_population = []
        for _ in range(self.size):
            # Selection: Use native random.choices
            parent = random.choices(self.population, weights=fitnessList, k=1)[0]

            # Clone and mutate
            child = copy.deepcopy(parent)
            child.mutate(probability=0.2)
            new_population.append(child)

        self.population = new_population
        self.best_individual = max(self.population, key=lambda ind: ind.fitness)


# --- MAP CONFIGURATION WITH PANDAS ---
city_names = ["A", "B", "C", "D", "E"]
adjacency_matrix = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 18],
    [15, 35, 0, 30, 5],
    [20, 25, 30, 0, 15],
    [25, 18, 5, 15, 0],
]

map_df = pd.DataFrame(adjacency_matrix, index=city_names, columns=city_names)

Popu = Population(map_df, size=100, start_node="A")

for _ in range(1000):
    Popu.evolve()

print(f"\nMejor ruta encontrada: {Popu.best_individual.route}")
print(f"Distancia Total: {Popu.best_individual.distance} km")
print(f"Aptitud: {Popu.best_individual.fitness:.6f}")

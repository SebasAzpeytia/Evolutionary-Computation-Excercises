import random

TARGET = "este es un ejemplo de una palabra mas grande"
GENES = "abcdefghijklmnopqrstuvwxyz "


class DNA:
    def __init__(self, gen=None):
        # Si no recibe genes, genera unos al azar (para la primera generación)
        if gen:
            self.gen = gen
        else:
            self.gen = [random.choice(GENES) for _ in range(len(TARGET))]

        self.score = 0
        self.calculate_fitness()

    def calculate_fitness(self):
        # Calculamos cuántas letras coinciden exactamente
        self.score = 0
        for target_letter, gen_letter in zip(TARGET, self.gen):
            if target_letter == gen_letter:
                self.score += 1

        # El fitness es el porcentaje de acierto.
        # Elevamos al cuadrado para darle mucho más "peso" a los mejores en la ruleta.
        porcentaje = self.score / len(TARGET)
        self.fitness = porcentaje**2

    def crossover(self, partner):
        # Cruce de un solo punto al azar
        mid = random.randint(0, len(self.gen))

        # Tomamos la primera mitad de la madre y la segunda mitad del padre
        child_gen = self.gen[:mid] + partner.gen[mid:]
        return DNA(child_gen)

    def mutate(self, prob_mutate=0.01):
        # Recorremos cada gen evaluando si muta o no
        for i in range(len(self.gen)):
            if random.random() <= prob_mutate:
                self.gen[i] = random.choice(GENES)

        # Si mutó, es necesario recalcular su calificación
        self.calculate_fitness()


class Population:
    def __init__(self, size=100, prob_mutate=0.01):
        self.size = size
        self.prob_mutate = prob_mutate
        self.population = [DNA() for _ in range(size)]
        self.best_individual = self.population[0]

    def evolve(self):
        # 1. Encontrar al mejor individuo de la generación actual
        self.best_individual = max(self.population, key=lambda ind: ind.score)

        # 2. Preparar los pesos para la ruleta
        # Extraemos todos los fitness para usarlos como probabilidades
        pesos = [ind.fitness for ind in self.population]

        new_population = []
        for _ in range(self.size):
            # 3. Selección por Ruleta Nativa
            # random.choices elige elementos de una lista basándose en sus pesos (fitness)
            parent_a = random.choices(self.population, weights=pesos, k=1)[0]
            parent_b = random.choices(self.population, weights=pesos, k=1)[0]

            # 4. Cruce y Mutación
            child = parent_a.crossover(parent_b)
            child.mutate(self.prob_mutate)

            new_population.append(child)

        # 5. Reemplazar la vieja generación con la nueva
        self.population = new_population


# --- EJECUCIÓN DEL ALGORITMO ---

generations = 9000
population_size = 1000
mutation_rate = 0.03

# Inicializamos el entorno
ecosystem = Population(size=population_size, prob_mutate=mutation_rate)

for i in range(generations):
    ecosystem.evolve()

    # Imprimir el progreso cada 100 generaciones
    if i % 100 == 0:
        palabra_actual = "".join(ecosystem.best_individual.gen)
        print(f"Gen {i}: {palabra_actual} | Score: {ecosystem.best_individual.score}")

    # Condición de paro temprano si ya encontró la palabra perfecta
    if ecosystem.best_individual.score == len(TARGET):
        print(f"\n¡Objetivo alcanzado en la generación {i}!")
        break

# Resultado Final
print("\n--- RESULTADO FINAL ---")
print("Palabra: ", "".join(ecosystem.best_individual.gen))
print("Score:   ", ecosystem.best_individual.score)

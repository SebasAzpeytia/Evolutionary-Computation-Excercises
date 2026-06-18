import random
from abc import ABC, abstractmethod
from monkeyTheorem.DNA import DNA


class selectPopulationMethod(ABC):
    @abstractmethod
    def selectPopulation(self, population: list[DNA]) -> list[DNA]:
        pass


class selectPopulationByMaxValues(selectPopulationMethod):
    def selectPopulation(self, population):
        potentialPopulation = sorted(population, key=lambda x: x.score, reverse=True)[
            0 : len(population)
        ]
        return potentialPopulation


class selectPopulationByRouletMethod(selectPopulationMethod):
    def selectPopulation(self, population: list[DNA]) -> list[DNA]:
        matingPool = self.generateMatingPool(population)
        potentialPopulation = random.choices(matingPool, k=100)
        return potentialPopulation

    def generateMatingPool(self, population: list[DNA]) -> list[DNA]:
        matingPool = []
        for character in population:
            quantity = int(character.fitness * 100)
            for _ in range(quantity**2):
                matingPool.append(character)

        return matingPool


class crossNewPopulation:
    def crossNewPopulation(self, population: list[DNA], probMutate=0.1):
        newChildsPopulation = []
        for i in range(len(population)):
            parentA, parentB = population[0], population[1]
            child = parentA.crossover(parentB)
            child.mutate(probMutate)
            newChildsPopulation.append(child)
            random.shuffle(population)
        return newChildsPopulation


class processGeneticAlgorithm:
    def __init__(
        self,
        selectPopulation: selectPopulationMethod,
        crossNewPopulationMethod: crossNewPopulation,
    ):
        self.targedSelected = None
        self.selectPopulation = selectPopulation
        self.crossNewPopulationMethod = crossNewPopulationMethod
        self.population = []

    def calculateTarget(self, iter=10, n_pob=100, probMutate=0.1):
        self.generateInitialPoblation(n_pob)  # Inicializar poblacion

        for i in range(iter):
            # Seleccionar Poblacion
            selectedPopulation = self.selectPopulation.selectPopulation(self.population)

            # Cruzar Poblacion
            newPopulationCrossed = self.crossNewPopulationMethod.crossNewPopulation(
                selectedPopulation, probMutate
            )

            # Nueva Poblacion Inicial
            self.population = newPopulationCrossed

        self.targedSelected = max(self.population, key=lambda x: x.score)

    def generateInitialPoblation(self, n_pob) -> list[DNA]:
        self.population = [DNA() for _ in range(n_pob)]

    def printPopulation(self):
        for i in self.population:
            print(i.gen)
            print(i.score)


selectPopulation = selectPopulationByRouletMethod()
crossNewPopulationMethod = crossNewPopulation()

GA = processGeneticAlgorithm(selectPopulation, crossNewPopulationMethod)
GA.calculateTarget(iter=9000, n_pob=1000, probMutate=0.03)

print("".join(GA.targedSelected.gen))
print(len(GA.targedSelected.gen))
print(GA.targedSelected.score)

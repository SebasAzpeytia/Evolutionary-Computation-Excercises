import random
import copy


class DNA:
    def __init__(self, matrixAdy: list[list[int]], startPos=0):
        self.matrixAdy = matrixAdy
        self.startPos = startPos
        self.routes = self.initializeRoutes()
        self.score = self.calculateScore()
        self.fitness = 0

    # Funcion para calcular la puntuacion individual del individuo
    def calculateScore(self):
        distance = 0
        for index in range(len(self.routes) - 1):
            actualRoute = self.routes[index]  # Obtenemos el nodo actual
            nextRoute = self.routes[index + 1]  # Obtenemos el siguiente nodo

            # Calculamos la distancia entre ambos nodos obteniendo su posicion en la matriz de adyacencia
            distance += self.matrixAdy[actualRoute][nextRoute]

        # Retornamos el inverso de la distancia (a mayor distancia menor Score)
        return 1 / distance

    # El fitness se calculará en funcion del score individual y el total (para generarlo en un rango de 0 a 1)
    def setFitness(self, totalScore):
        self.fitness = self.score / totalScore

    # Funcion para inicializar la primer ruta aleatoria por defecto
    def initializeRoutes(self):
        longMatrixAdy = len(self.matrixAdy[0])  # Cantidad de paradas en la ruta

        # Generando lista con ruta al azar usando funcion sample()
        initialRoute = random.sample(range(0, longMatrixAdy), longMatrixAdy)

        # Eliminando el elemento que corresponda al inicio y fin de la ruta (iran al final)
        initialRoute.remove(self.startPos)

        # Retornamos la ruta establecida concatenando la posicion inicial y final
        return [self.startPos] + initialRoute + [self.startPos]

    # Nota educativa: Lo que hace este método matemáticamente es una Mutación (intercambio de genes), no un Crossover.
    def crossover(self, crossRate=0.01):
        if crossRate < random.random():
            index1 = random.randint(1, len(self.routes) - 2)
            index2 = random.randint(1, len(self.routes) - 2)

            self.routes[index1], self.routes[index2] = (
                self.routes[index2],
                self.routes[index1],
            )
            # REPARACIÓN: Es crucial recalcular el score después de modificar la ruta
            self.score = self.calculateScore()


class Population:
    def __init__(self, DNATemplate: DNA, matrixAdy, quantity=100, startPos=0):
        self.DNATemplate = DNATemplate
        self.targetSelected = None
        self.quantity = quantity
        self.popu = [DNATemplate(matrixAdy, startPos) for _ in range(quantity)]
        self.totalScore = 0  # Se inicializa en 0, se calculará en run()

    def run(self, generations=10):
        for _ in range(generations):
            self.totalScore = sum(ind.score for ind in self.popu)
            self.precalculateFitness()
            self.updatePopulation()

        self.targetSelected = max(self.popu, key=lambda ind: ind.fitness)

    def precalculateFitness(self):
        [ind.setFitness(self.totalScore) for ind in self.popu]

    def updatePopulation(self):
        newPopulation = []
        for i in range(len(self.popu)):
            parent = self.selectIndividual()
            children = copy.deepcopy(parent)
            children.crossover()
            newPopulation.append(children)

        self.popu = newPopulation

    def selectIndividual(self):
        selectedFitness = random.random()
        acumulated = 0
        for ind in self.popu:
            acumulated += ind.fitness
            if acumulated >= selectedFitness:
                return ind
        # Fallback de seguridad por si hay errores de precisión de decimales en Python
        return self.popu[-1]


matrix = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 18],
    [15, 35, 0, 30, 5],
    [20, 25, 30, 0, 15],
    [25, 18, 5, 15, 0],
]

population = Population(DNA, matrix, quantity=100, startPos=0)
population.run(generations=100)

print(f"Mejor Ruta Encontrada: {population.targetSelected.routes}")
print(f"Score: {population.targetSelected.score}")

# 0 1 3 4 2 0

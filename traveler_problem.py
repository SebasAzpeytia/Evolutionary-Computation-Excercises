import random


class Graph:
    pass


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weigth):
        self.add_node(u)
        self.add_node(v)

        self.graph[u].append((v, weigth))
        # self.graph[v].append((u, weigth))

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def generate_graph_by_matrix(self, matrix: list[list[int]]) -> Graph:
        for index, row in enumerate(matrix):
            for indexItem, item in enumerate(row):
                self.add_edge(str(index), str(indexItem), item)

    def search_path_weigth(self, u, v):
        if u > len(self.graph):
            return None
        row = self.graph[str(u)]
        if v > len(row):
            return None

        return dict(row)[str(v)]

    def __str__(self):
        return str(self.graph)


class DNA:
    def __init__(self, graph: Graph, start_pos=0):
        self.routes = self.initialize_DNA(start_pos)
        self.distance = self.calculateDistance(graph)
        self.graph = graph

    def initialize_DNA(self, start_pos):
        routes = []
        while len(routes) < 4:
            value = random.randint(0, 4)
            if (value not in routes) and (value != start_pos):
                routes.append(value)
        return [start_pos] + routes + [start_pos]

    def calculateDistance(self, graph: Graph):
        distance = 0

        for i in range(len(self.routes) - 1):
            actualPosition = self.routes[i]
            nextPosition = self.routes[i + 1]

            distance += graph.search_path_weigth(actualPosition, nextPosition)

        return distance

    def crossover(self, crossRate=0.01):
        if crossRate < random.random():
            index1 = random.randint(1, len(self.routes) - 2)
            index2 = random.randint(1, len(self.routes) - 2)

            self.routes[index1], self.routes[index2] = (
                self.routes[index2],
                self.routes[index1],
            )
            self.distance = self.calculateDistance(self.graph)


class Population:
    def __init__(self, graph, quantity=10, start_pos=0, crossRate=0.01):
        self.popu = [DNA(graph, start_pos) for _ in range(quantity)]
        self.targetSelected = None
        self.totalDistance = self.calculateTotalDistance()
        self.crossRate = crossRate

    def selection(self):
        matingPool = self.generate_MatingPool()
        for index, _ in enumerate(self.popu):
            self.popu[index] = matingPool[0]
            random.shuffle(matingPool)

    def generate_MatingPool(self) -> list[DNA]:
        matingPool = []

        for individual in self.popu:
            individual.crossover(self.crossRate)
            nTimes = int(self.calculateFitness(individual))
            for _ in range(nTimes):
                matingPool.append(individual)

        return matingPool

    def calculateFitness(self, individual: DNA):
        fitness = self.totalDistance / individual.distance
        return fitness

    def calculateTotalDistance(self):
        totalDistance = 0
        for element in self.popu:
            totalDistance += element.distance
        return totalDistance

    def run(self, generations=10):
        for _ in range(generations):
            self.selection()

        self.targetSelected = min(self.popu, key=lambda x: x.distance)


matrix = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 18],
    [15, 35, 0, 30, 5],
    [20, 25, 30, 0, 15],
    [25, 18, 5, 15, 0],
]

G = Graph()
G.generate_graph_by_matrix(matrix)

popu = Population(G, quantity=20, start_pos=0, crossRate=0.01)
popu.run(generations=20)

# 0 1 3 4 2 0

print(popu.targetSelected.routes)
print(popu.targetSelected.distance)

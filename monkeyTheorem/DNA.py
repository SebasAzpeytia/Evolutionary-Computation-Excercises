import random

target = "este es un ejemplo de una palabra mas grande"


class DNA:
    pass


class DNA:
    def __init__(self):
        self.gen = [
            random.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(len(target))
        ]

    @property
    def fitness(self) -> float:
        score = 0
        for letterTarget, letterGen in zip(target, self.gen):
            if letterTarget == letterGen:
                score += 1

        return score / len(self.gen)

    @property
    def score(self):
        score = 0
        for letterTarget, letterGen in zip(target, self.gen):
            if letterTarget == letterGen:
                score += 1

        return score

    def crossover(self, parent: DNA) -> DNA:
        middlePoint = len(parent.gen) // 2
        middlePoint += random.randint(-6, 6)
        # middlePoint = random.randint(1, len(parent.gen))
        motherGen = self.gen
        child = DNA()

        child.gen[0:middlePoint] = motherGen[0:middlePoint]
        child.gen[middlePoint:-1] = parent.gen[middlePoint:-1]
        return child

    def mutate(self, probMutate=0.1):
        for index, _ in enumerate(self.gen):
            if random.random() <= probMutate:
                self.gen[index] = random.choice("abcdefghijklmnopqrstuvwxyz ")

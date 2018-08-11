##To-Do 8/10
#-Need to add lottery
#-more elegant path generation

import graph
import random

def populate(start_node, size, graph):
    population = []
    for i in range(1, size+1):
        temp = Genetic_Sales(start_node, i)
        temp.create_path(graph)
        population.append(temp)
    return population

def lottery(population, graph):
    size = len(population)
    coeff = float(1.0 / size)
    ind = int(0.1 * size)
    start = population[0].start_node
    population = sorted(population, key=lambda x: x.fitness)
    for i in range(0,size):
        if i in range(0, int(0.5*ind)):
            new_member = Genetic_Sales(start, size-i)
            new_member.crossover(population[i], population[random.randint(0, size - 2 * ind - i)], graph)
            population[size-i-1] = new_member
        elif i in range(int(9*ind), int(9.5*ind)):
            new_member = Genetic_Sales(start, size - i)
            new_member.create_path(graph)
            population[i] = new_member
    return population

class Genetic_Sales:
    def __init__(self, start_node, id):
        self.start_node = start_node
        self.ID = id
        self.path = [start_node.name]
        self.weights = []
        self.fitness = 0
        self.score = 0

    def __str__(self):
        return "ID: {}\nPath: {}\nFitness: {}"\
            .format(self.ID, self.path, self.fitness)

    def crossover(self, parent1, parent2, graph):
        flag = True
        for node in parent1.path:
            self.path.append(node)
            if node in parent2.path:
                index = parent2.path.index(node)
                self.path = parent1.path[:index] + parent2.path[index:]
                self.weights = parent1.weights[:index] + parent2.weights[index:]
                self.fitness = int(sum(self.weights))
                flag = False
                break
        if flag:
            self.gen_path(parent1, graph)

    def gen_path(self, parent, graph):
        rand_int = random.randint(1,len(parent.path)-1)
        self.path = parent.path[:rand_int]
        while True:
            curr_index = graph.get_index_by_name(self.path[-1])
            [next_connect, next_weight] = graph.nodes[curr_index].next_node(self.path)
            if next_connect == self.start_node.name:
                self.fitness = int(sum(self.weights))
                break
            else:
                self.path.append(next_connect)
                self.weights.append(next_weight)

    def create_path(self, graph):
        while True:
            index = graph.get_index_by_name(self.path[-1])
            [next_connect, next_weight] = graph.nodes[index].next_node(self.path[1:])
            if next_connect == None:
                self.path = [self.start_node.name]
                self.weights = []
            else:
                self.path.append(next_connect)
                self.weights.append(next_weight)
                if next_connect == self.start_node.name:
                    self.fitness = int(sum(self.weights))
                    break

if __name__ == "__main__":
    graph = graph.Graph("large_test_nodes")
    population = populate(graph.nodes[0], 100, graph)
    for i in range(100000):
        population = lottery(population, graph)
        if i % 10000 == 0:
            print("Alpha:\n{} ".format(population[0]))
            avg = 0
            size = len(population)
            for x in population:
                avg += x.fitness
            avg = float(avg/size)
            print("Average Fitness = {}\n".format(avg))
##To-Do 8/10
#-Need to add lottery
#-Need to add mandatory nodes
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

def lottery(population):
    pass

class Genetic_Sales:
    def __init__(self, start_node, id):
        self.start_node = start_node
        self.ID = id
        self.path = [start_node.name]
        self.weights = []
        self.fitness = []

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
                self.fitness = sum(self.weights)
                flag = False
                break
        if flag:
            self.gen_path(parent1, graph)

    def gen_path(self, parent, graph):
        rand_int = random.randint(0,len(parent.path)-1)
        self.path = parent.path[:rand_int]
        while True:
            curr_index = graph.get_index_by_name(self.path[-1])
            [next_connect, next_weight] = graph.nodes[curr_index].next_node(self.path)
            if next_connect == self.start_node.name:
                break
            else:
                self.path.append(next_connect)
                self.weights.append(next_weight)
        self.fitness = sum(self.weights)

    def create_path(self, graph):
        while True:
            index = graph.get_index_by_name(self.path[-1])
            print(self.path[-1])
            if len(self.path) > 1:
                if self.path[-2] == self.start_node.name:
                    [next_connect, next_weight] = graph.nodes[index].next_node(self.path)
                else:
                    [next_connect, next_weight] = graph.nodes[index].next_node(self.path[1:])
            else:
                [next_connect, next_weight] = graph.nodes[index].next_node(self.path[1:])
            if next_connect == None:
                self.path = [self.start_node.name]
            else:
                if next_connect == self.start_node.name:
                    self.path.append(next_connect)
                    self.weights.append(next_weight)
                    break
                else:
                    self.path.append(next_connect)
                    self.weights.append(next_weight)
        self.fitness = sum(self.weights)


if __name__ == "__main__":
    graph = graph.Graph("test_nodes.txt")
    population = populate(graph.nodes[0], 5, graph)
    for item in population:
        print(item)
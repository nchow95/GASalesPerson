import random

class Node:
    def __init__(self, name, connections, weights):
        self.connections = connections
        self.name = name
        self.weights = weights
        if len(connections) != len(weights):
            raise ValueError("Connections and Weights need to be the same")
        self.edges = len(connections)

    def __str__(self):
        return "Name: {}\n Connections: {}\n Weights{}\n"\
            .format(self.name, self.connections, self.weights)

    def next_node(self, past_nodes):
        rand_index = random.randint(0, self.edges-1)
        flag = True
        while True:
            if self.connections[rand_index] in past_nodes:
                if (rand_index + 1) < self.edges:
                    rand_index += 1
                else:
                    if flag:
                        rand_index = 0
                        flag = False
                    else:
                        return [None, None]
            else:
                return [self.connections[rand_index], self.weights[rand_index]]
                break

class Graph:
    def __init__(self, filename):
        self.nodes = []
        self.parsefile(filename)

    def parsefile(self, filename):
        with open(filename) as file:
            file_lines = file.readlines()
        for line in file_lines:
            connections = []
            weights = []
            [name, connection_str] = line.split(" = ")
            connect_items = connection_str[2:-3].split("), (")
            if len(connect_items) == 1:
                [connection, weight] = connection_str[2:-3].split(", ")
                connections.append(connection)
                weights.append(int(weight))
            else:
                for item in connect_items:
                    [connection, weight] = item.split(", ")
                    connections.append(connection)
                    weights.append(int(weight))
            self.nodes.append(Node(name, connections, weights))

    def get_index_by_name(self, name):
        index = 0
        for node in self.nodes:
            if node.name == name:
                return index
            index += 1

import re

class Graph:
    def __init__(self, filename):
        self.filename = filename
        self.adjacencyList={}
        self.n=0
        try:
            with open(filename, 'r') as file:
                data = file.read().split('\n')

                self.checkFileFormat(data)
                self.buildGraph(data)
                hasCycle = self.checkGraph()
                if hasCycle:
                    raise Exception("Graph is cyclic")

        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def checkFileFormat(self, data):
        if not bool(re.match(r'^\s*-?\d+\s*$', data[0])):
            raise Exception('Graph format not supported: Line 0: ', data[0])
        for el in data[1:]:
            if not bool(re.match(r'^\s*\d+\s+\d+\s*$', el) or re.match(r'^\s*$', el)):
                raise Exception('Graph format not supported: ', el)
            
    def buildGraph(self, data):

        self.n=int(data[0])

        for el in range(0, self.n):
            if el not in self.adjacencyList:
                    self.adjacencyList[el] = []

        for el in data[1:]:
            temp=el.split()
            if temp==[]:
                return
            temp=[int(a)-1 for a in temp]
            if temp[0] not in self.adjacencyList:
                self.adjacencyList[temp[0]] = []

            if temp[1] not in self.adjacencyList[temp[0]]:
                self.adjacencyList[temp[0]].append(temp[1])
        
    def checkGraph(self):
        visited = set()
        recursion_stack = set()
        has_cycle = False

        for vertex in self.adjacencyList:
            if vertex not in visited:
                if self.dfs_cycle_detection(vertex, visited, recursion_stack):
                    has_cycle = True

        return has_cycle

    def dfs_cycle_detection(self, vertex, visited, recursion_stack):
        visited.add(vertex)
        recursion_stack.add(vertex)

        # Traverse neighbors
        for neighbor in self.adjacencyList.get(vertex, []):
            if neighbor not in visited:
                if self.dfs_cycle_detection(neighbor, visited, recursion_stack):
                    return True
            elif neighbor in recursion_stack:
                return True

        recursion_stack.remove(vertex)
        return False
        
# g=Graph('configs\graph.txt')

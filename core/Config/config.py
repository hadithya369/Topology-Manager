import json
from .graph import Graph

class Configuration:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(filename, 'r') as file:
                self.data = json.load(file)

                self.checkJsonGraph()

                self.createGraph()

                self.checkLLM()
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file '{filename}' does not contain valid JSON.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def checkJsonGraph(self):
        if 'graph' not in self.data.keys():
            raise Exception("Missing key 'graph' in configuration file")
        if 'path' not in self.data['graph'].keys():
            raise Exception("Missing key 'path' for 'graph'")
        
    def createGraph(self):
        self.graph=Graph(self.data['graph']['path'])

    def checkLLM(self):
        if 'LLM' not in self.data.keys():
            raise Exception("Missing key 'LLM' in configuration file")
        
        llmList=self.data['LLM']
        checklist=[1 for e in range(0,self.graph.n)]

        for el in llmList:
            if (el['id']-1)<0 or (el['id']-1)>=self.graph.n:
                raise Exception("ID's not present in range: 1 to "+str(self.graph.n))
            checklist[el['id']-1]-=1
        if sum(checklist)!=0:
            raise Exception("ID's not present in range 1 to "+str(self.graph.n))


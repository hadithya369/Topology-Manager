from ..Config.config import Configuration
from .instruction import Instruction
from ..Models.llmlist import LLMList
import json

class InstructionExecutor:
    def __init__(self, configfile):
        self.configfile = configfile
        self.config = Configuration(configfile)
        self.llmList = LLMList()
        self.topologicalSequence()
        self.buildReverseGraph()
        self.populateLlmList(self.config.data['LLM'])

    def populateLlmList(self, paramList):
        for el in paramList:
            self.llmList.addLLM(el)

    def topologicalSequenceUtil(self, i, vis, stk):
        vis[i]=True
        for el in self.config.graph.adjacencyList[i]:
            if vis[el]!=True:
                self.topologicalSequenceUtil(el, vis, stk)
        stk.append(i)

    def topologicalSequence(self):
        self.executionSequence=[]
        vis=[False for e in range(self.config.graph.n)]

        for i in range(self.config.graph.n):
            if vis[i]==False:
                self.topologicalSequenceUtil(i, vis, self.executionSequence)

        self.executionSequence.reverse()

    def buildReverseGraph(self):
        self.reverseAdjacencyList={}
        for el in range(self.config.graph.n):
            self.reverseAdjacencyList[el]=[]

        for el in self.config.graph.adjacencyList:
            memberList=self.config.graph.adjacencyList[el]

            for i in memberList:
                if el not in self.reverseAdjacencyList[i]:
                    self.reverseAdjacencyList[i].append(el)
        # print(self.reverseAdjacencyList)


    def executeInstruction(self, query):
        memory={}

        for el in self.executionSequence:
            temp = Instruction(query)
            for i in self.reverseAdjacencyList[el]:
                temp.pushInstruction(memory[i+1])
            tempInstruction = temp.getInstruction()
            print(f'Instruction for {el+1}: {tempInstruction}')
            memory[el+1]=self.llmList.predict(el+1, tempInstruction)
            # memory[el] = self.llmList.predict(el, query)
        print('Printing memory')
        with open('D:\\data.json', 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=4)
        print(memory)



I = InstructionExecutor('configs/example.json')
I.executeInstruction('I have 100 apples. I gave 20 apples to my sister and 10 apples to my brother. How many apples do I have left?')
# print(I.)
from ..Config.config import Configuration
from .instruction import Instruction
from ..Models.llmlist import LLMList
import json
import logging
import time
logger = logging.getLogger(__name__)
logging.basicConfig(filename='D:/outputs/times.log', level=logging.INFO)

class InstructionExecutor:
    def __init__(self, configfile):
        self.configfile = configfile
        t1=time.time()
        self.config = Configuration(configfile)
        self.llmList = LLMList()
        self.topologicalSequence()
        self.buildReverseGraph()
        self.populateLlmList(self.config.data['LLM'])
        self.history={}
        logger.info(f'[Init time]: {time.time()-t1}')

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
            # print(f'Instruction for {el+1}: {tempInstruction}')
            if el+1 in self.history.keys():
                past=self.history[el+1]  
            else:
                past=''
                self.history[el+1]=''

            memory[el+1]=self.llmList.predict(el+1, f'Predict the next episode in this Memory Sequence: {past}\nQuery: {tempInstruction}\n')
            self.history[el+1]+=f'\n\nNext Episode: {memory[el+1]}'
            # memory[el] = self.llmList.predict(el, query)
            
            
        return {'query':query, 'memory':memory}

    def executeInstructionSequence(self, querylist):

        for i, q in enumerate(querylist):
            print(f'Executing Instruction: {i}')
            t1=time.time()
            temp=self.executeInstruction(q)
            logger.info(f'[Topology time]: {time.time()-t1}')

            with open(f'D:/outputs/data{i}.json', 'w', encoding='utf-8') as f:
                json.dump(temp, f, ensure_ascii=False, indent=4)    

        with open(f'D:/outputs/history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)    
            
        


I = InstructionExecutor('configs/example.json')
instr='Behave like you are this subsystem and generate the outputs as specified and provide one of the outputs you are created to generate. Dont summarize your responsibilities in the description just your output in the format you are told to produce. No need to give a detailed explaination'
instrlist=[instr for el in range(8)]
I.executeInstructionSequence(instrlist)
# I.executeInstructionSequence(['Behave like you are this subsystem and generate the outputs as specified and provide one of the outputs you are created to generate. Dont summarize your responsibilities in the description just your output in the format you are told to produce. No need to give a detailed explaination'])
# I.executeInstruction('Behave like you are this subsystem and generate the outputs as specified and provide one of the outputs you are created to generate. Dont summarize your responsibilities in the description just your output in the format you are told to produce. No need to give a detailed explaination')
# I.executeInstruction('I have 100 apples. I gave 20 apples to my sister and 10 apples to my brother. How many apples do I have left?')
# I.executeInstruction('There are 10 crows on an electric line. If a hunter shoots the leftmost crow and it falls to the ground, how many crows will be left on the electric line?')
# I.executeInstruction('Statements: All trucks fly. Some scooters fly. Conclusions: All trucks are scooters. Some scooters do not fly. Which of the conclusions are correct according to the statements? answer it like an assertion reasoning question and make reasonable assumptions')
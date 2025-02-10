from .llm import LLM, LocalLLM
import os
import logging
import time
logger = logging.getLogger(__name__)
logging.basicConfig(filename='D:/outputs/times.log', level=logging.INFO)

class LLMList:
    def __init__(self):
        self.llms = {}
        self.llmInstructions = {}

    def addLLM(self, params):
        if params['id'] in self.llms.keys():
            return False
        if 'apikeypath' not in params.keys():
            self.llms[params['id']]=LocalLLM(params['id'])
            self.llmInstructions[params['id']]=params['instruction']
            return True
        if not os.path.exists(params['apikeypath']):
            return False
            
        
        with open(params['apikeypath'], 'r') as f:
            apiKey = f.read()
        
        self.llms[params['id']]=LLM(params['id'], apiKey)
        self.llmInstructions[params['id']]=params['instruction']
        return True
    
    def predict(self, id, query):
        return self.llms[id].predict(self.llmInstructions[id]+'\n'+query)

    # def predict(self, id, query):
    #     t1=time.time()
    #     logger.info(f'[LLM Inference time]: {time.time()-t1}')
    #     return query+'\nasdfsdfsdafsf'

# llist = LLMList()
# llist.addLLM(
#     {
#         "id": 1,
#         "name": "mistralai/mistral-7b-instruct",
#         "apikeypath": "D:\\CS297\\openrouter.txt",
#         "instruction": "provide the answer with text reversed",
#     }
# )
# print(llist.predict(1, 'What is the deepest point in the pacific ocean?'))
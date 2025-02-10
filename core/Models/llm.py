import requests
import json
import time
from openai import OpenAI
from ..DB.scrape import SearchTool
from ..DB.vecdb import VectorSearch
import logging
import time
logger = logging.getLogger(__name__)
logging.basicConfig(filename='D:/outputs/times.log', level=logging.INFO)

class LLM:
    def __init__(self, id, apiKey):
        self.id = id
        self.apiKey = apiKey
    
    def predict(self, query):
        time.sleep(2)
        t1=time.time()
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.apiKey}",
            },
            data=json.dumps({
                # "model": "mistralai/mistral-7b-instruct:free",
                "model": "meta-llama/llama-3.2-3b-instruct:free",
                "messages": [
                {
                    "role": "user",
                    "content": query
                }
                ]
                
            })
        )
        logger.info(f'[LLM Inference time]: {time.time()-t1}')

        if response.status_code==200:
            return response.json()['choices'][0]['message']['content']
        return 'API failure - Response code: '+str(response.status_code)
    

class LocalLLM:

    def __init__(self, id):
        self.id = id
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        self.searchTool = SearchTool()

    def predictInternet(self, query):
        response1=self.queryLLM(query)
        response=self.queryLLM(response1+'\nDoes the content above say it needs to access realtime information from the web?(Answer only with yes or no)')
        # print('Response Needed?: '+response)
        # Internet not needed
        if response.startswith('No'):
            return response1
        # otherwise
        response=self.queryLLM(query+'\nGive me a single google search phrase that will help answer this question. nothing else')
        # searchTopics= response.split('\n')
        print('Searching web: ', response)
        vals=self.searchTool.search([response])[:20]
            # print(vals)
        print('Embedding results')
        v=VectorSearch(vals)
        info=v.query(query, 4)
        print(info)
        infos=''
        for i in info:
            infos+=' '+i
        response=self.queryLLM(infos+'\n'+'Use the above information and answer this query.\n'+query)
        print(response)
        return response
    
    def queryLLM(self, query):

        completion = self.client.chat.completions.create(
            model="lmstudio-community/Llama-3.2-3B-Instruct-GGUF",
            messages=[
                {"role": "system", f"content": "Answer the question as accurately as possible"},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
        )

        return completion.choices[0].message.content
        # if response.status_code==200:
        #     return response.json()['choices'][0]['message']['content']
        # return 'API failure - Response code: '+str(response.status_code)
    def predict(self, query):
        # print('predicting: ', query)
        return self.predictInternet(query)

# temp = LocalLLM(0)
# print(temp.predictInternet('I have 100 apples. I gave 40 apples to my brother and 10 apples to my sister. How many apples do I have left?'))
# print(temp.predictInternet('What is the price of google stock today'))
# print(temp.predict('Who is the presidential candidates of us elections 2024?'))
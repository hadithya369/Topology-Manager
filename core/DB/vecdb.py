import pandas as pd
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from lancedb.embeddings import TextEmbeddingFunction
from openai import OpenAI
from lancedb.embeddings.registry import register
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import EmbeddingFunctionRegistry

db = lancedb.connect("/tmp/db")


@register("sentence-transformers")
class SentenceTransformerEmbeddings(TextEmbeddingFunction):
    name: str = "myspeciall"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ndims = None

    def generate_embeddings(self, texts):
        embedList=[]
        
        if type(texts)!=type(['']):
            return [self._embedding_model().embeddings.create(input = [texts], model=self._model_name()).data[0].embedding]
        for text in texts:
            text = text.replace("\n", " ")
            embedList.append(self._embedding_model().embeddings.create(input = [text], model=self._model_name()).data[0].embedding)
            
        return embedList

    def ndims(self):
        if self._ndims is None:
            self._ndims = len(self.generate_embeddings("foo")[0])
        return self._ndims
    
    def _embedding_model(self):
        return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    
    def _model_name(self):
        return "nomic-ai/nomic-embed-text-v1.5-GGUF"
    
class VectorSearch:
    def __init__(self, data):
        self.data=data
        self.registry = EmbeddingFunctionRegistry.get_instance()
        self.stransformer = self.registry.get("sentence-transformers").create(name='myspeciall')
        self.size=self.stransformer.ndims()

        class TextModelSchema(LanceModel):
            vector: Vector(self.size) = self.stransformer.VectorField()
            text: str = self.stransformer.SourceField()
        
        db.drop_table('table')
        self.tbl = db.create_table("table", schema=TextModelSchema)
        self.tbl.add(pd.DataFrame({"text": data}))

    def query(self, query, k):
        result = self.tbl.search(query).limit(k).to_list()
        response=[]
        for res in result:
            response.append(res['text'])
        return response
    
# v=VectorSearch(['Qualcomm announced its latest smartphone chip packed with AI features.On Sunday, an analyst expressed doubts about', 'AAPLApple, Inc. engages in the design, manufacture, and sale of smartphones, personal computers, tablets, wearables and accessories, and other varieties of related', 'When Q3 earnings reports come in, Apple investors will focus on wireless subscriber upgrades to iPhone 16 models.'])
# print(v.query('iphone', 3))

    

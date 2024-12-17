from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
import pdb

class DataRetriever():
    def __init__(self,cfg,llm=None,preprocessed_data=None,vector_store=None) -> None:
        self.perform_sparse_search = cfg["retriever_details"]["sparse_search"]["perform_search"]
        self.perform_semantic_search = cfg["retriever_details"]["semantic_search"]["perform_search"]
        self.perform_multiquery_search = cfg["retriever_details"]["multiquery_search"]["perform_search"]
        self.sparse_search_method = cfg["retriever_details"]["sparse_search"]["search_method"]
        self.semantic_search_search_type = cfg["retriever_details"]["semantic_search"]["search_method"]
        self.topk = cfg["retriever_details"]["topk"]
        self.llm = llm
        self.preprocessed_data = preprocessed_data
        self.vector_store = vector_store
        self.retriever = None
    
    def generate_retriever(self):

        # pdb.set_trace()

        sparse_search = None
        if self.perform_sparse_search:
            if self.sparse_search_method == 'bm25':
                if self.preprocessed_data != None:
                    sparse_search = BM25Retriever.from_documents(self.preprocessed_data)
                    sparse_search.k = self.topk
                else:
                    print("Please provide the documents for generating the retriever")
        
        semantic_search = None
        if self.perform_semantic_search:
            if self.vector_store != None:
                if self.semantic_search_search_type == "similarity":
                    semantic_search = self.vector_store.as_retriever(search_type=self.semantic_search_search_type,search_kwargs={"k": self.topk})
                elif self.semantic_search_search_type == "mmr":
                    print("we are yet to implement mmr")
            else:
                print("Please provide a vector store for semantic retrival")
        
        if self.perform_multiquery_search:
            if semantic_search != None:
                #can also add prompt configurations here
                semantic_search = MultiQueryRetriever.from_llm(retriever=semantic_search,llm=self.llm)
            else:
                print("please implement semantic search for multi query search")
        
        if sparse_search != None and semantic_search != None:
            self.retriever = EnsembleRetriever(retrievers=[sparse_search,semantic_search],weights=[0.3,0.7]) #need to make this weights configurable
        elif sparse_search != None and semantic_search == None:
            self.retriever = sparse_search
        elif sparse_search == None and semantic_search != None:
            self.retriever = semantic_search
        else:
            print("Please select one of the retriever")

        return self.retriever

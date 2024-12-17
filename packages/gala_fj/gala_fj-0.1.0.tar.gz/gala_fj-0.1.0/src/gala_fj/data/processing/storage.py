from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pickle
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import os
from gala_fj.data.graphs.triplet_generation import TripleExtractor
from gala_fj.data.graphs.kg_insertion import Neo4jKnowledgeGraphHandler

class DataStorage():
    def __init__(self,data,cfg):
        self.data = data
        self.vector_store = None
        self.embedding_model = None
        self.embedding_model_type = cfg["preprocessing_details"]["embedding_model"]
        self.chain_type = cfg["rag_chain_details"]["chain_type"]
        # print(self.data[1].metadata['chunk_id'])
        self.cfg = cfg

    
    def _tokenize_documents(self,documents):
        tokenized_docs = []
        for doc in documents:
            # Extract text from each Document object
            text = doc.page_content
            
            # Tokenize the text
            tokenized_text = [word.lower() for word in word_tokenize(text) if word.isalpha()]
            tokenized_docs.append(tokenized_text)

        return tokenized_docs
    
    def perform_storage(self, embeddings):
        
        if self.chain_type != "simple":
            if self.chain_type == "kg":
                if not os.path.exists(f'{self.cfg["cache_information"]["cache_folder_path_for_file"]}/triples.txt'):
                    triples_extractor = TripleExtractor(self.cfg)
                    for data in self.data:
                        triples_extractor.extract_triples(data.page_content,f'{self.cfg["cache_information"]["cache_folder_path_for_file"]}/triples.txt')
                        break
                neo4j_handler = Neo4jKnowledgeGraphHandler(self.cfg["graph_database_details"]["neo4j_uri"],
                                                self.cfg["graph_database_details"]["neo4j_user_name"],
                                                self.cfg["graph_database_details"]["neo4j_password"])
                neo4j_handler.process_single_file(file_path=f'{self.cfg["cache_information"]["cache_folder_path_for_file"]}/triples.txt')
                print("Inserted Triples")
                neo4j_handler.close()
            elif self.chain_type == "sem_kg":
                if not os.path.exists(f'{self.cfg["cache_information"]["cache_folder_path_for_file"]}/chunk_wise_triples'):
                    os.makedirs(f'{self.cfg["cache_information"]["cache_folder_path_for_file"]}/chunk_wise_triples')
                    folder_path = f'{self.cfg["cache_information"]["cache_folder_path_for_file"]}/chunk_wise_triples'
                    triples_extractor = TripleExtractor(self.cfg)
                    for data in self.data:
                        triples_extractor.extract_triples(data.page_content,f"{folder_path}/{data.metadata['chunk_id']}.txt")
                neo4j_handler = Neo4jKnowledgeGraphHandler(self.cfg["graph_database_details"]["neo4j_uri"],
                                                    self.cfg["graph_database_details"]["neo4j_user_name"],
                                                    self.cfg["graph_database_details"]["neo4j_password"])
                neo4j_handler.process_files_in_folder(folder_path=f'{self.cfg["cache_information"]["cache_folder_path_for_file"]}/chunk_wise_triples')
                print("Inserted Chunk wise triples Triples")
                neo4j_handler.close()
        if self.cfg["retriever_details"]["sparse_search"]["perform_search"] and self.cfg["retriever_details"]["sparse_search"]["search_method"] == "bm25":
            tokenized_data = self._tokenize_documents(self.data)
            bm25 = BM25Okapi(tokenized_data)
            
            bm25_save_path = os.path.join(self.cfg["cache_information"]["cache_folder_path_for_file"],'bm25_index.pkl')
            # Save the BM25 index to disk
            with open(bm25_save_path, 'wb') as f:
                pickle.dump(bm25, f)

        # Store Vectors in Chroma DB
        persist_directory = os.path.join(self.cfg["cache_information"]["cache_folder_path_for_file"],"chromadb")
        if os.path.exists(persist_directory):
            self.vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
            print("Loaded vector store from disk.")
        else:
            self.vector_store = Chroma.from_documents(documents=self.data, embedding=embeddings, persist_directory = persist_directory)
            self.vector_store.persist()
            print("Vector store created and saved to disk.")
        return self.vector_store
   

# if __name__ == '__main__':
#     dp = DataParser("https://lilianweng.github.io/posts/2023-06-23-agent/")
#     parsed_docs = dp.perform_parsing()
#     from smart_companion.data_preprocessing import DataPreprocessor
#     from smart_companion.data_storage import DataStorage
#     dpp = DataPreprocessor(parsed_docs)
#     pre_processed = dpp.perform_preprocessing()
#     vs = DataStorage(pre_processed)
#     vs_db = vs.perform_storage()

#     retriever = vs_db.as_retriever()
#     retrieved_docs = retriever.invoke("What are the approaches to Task Decomposition?")
#     print(retrieved_docs)

import yaml
import os
import pickle
from tqdm import tqdm
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
# from gala.utils.additional_functionalities import extract_urls
import pdb
import re



class DataPreprocessor:
    def __init__(self, data, cache_file="preprocessing_cache.pkl",cfg=None):
        """
        Initialize the DataPreprocessor with data, chunking parameters, and cache settings.
        
        :param data: The input data to be preprocessed.
        :param chunk_size: The size of each chunk.
        :param chunk_overlap: The overlap between chunks.
        :param cache_file: The file where preprocessed data will be cached.
        """
        self.data = data
        self.chunk_size = cfg["preprocessing_details"]["chunk_size"]
        self.chunk_overlap = cfg["preprocessing_details"]["chunk_overlap"]
        self.cache_file = cache_file
        self.preprocessed_data = []
        self.cfg = cfg
        self.save_metadata()

        # Determine the splitter type from configuration
        self.splitter_type = cfg["preprocessing_details"]["text_splitter"]
        print("---->",self.splitter_type)

    def extract_urls(self,text):
        url_pattern = r'URL Source:\s*(https?://\S+)'
        urls = re.findall(url_pattern, text)
        return urls if urls else ["No URLs found"]

    def save_metadata(self):
        for i in range(len(self.data)):
            url = self.extract_urls(self.data[i].page_content)[0]
            self.data[i].metadata['url'] = url
            self.data[i].metadata['file_index'] = i


    def load_cache(self):
        """
        Loads preprocessed data from the cache file if it exists.
        """

        cache_path = os.path.join(self.cfg["cache_information"]["cache_folder_path_for_file"],self.cache_file)

        if os.path.exists(cache_path):
            print(f"Loading cached data from {cache_path}")
            with open(cache_path, 'rb') as f:
                self.preprocessed_data = pickle.load(f)
            return True
        return False

    def save_cache(self):
        """
        Saves the preprocessed data to the cache file.
        """
        cache_path = os.path.join(self.cfg["cache_information"]["cache_folder_path_for_file"],self.cache_file)

        print(f"Caching preprocessed data to {cache_path}")

        with open(cache_path, 'wb') as f:
            pickle.dump(self.preprocessed_data, f)

    def preprocess_data(self, text_splitter, process_func):
        """
        Preprocesses the data using the provided text splitter and processing function.
        
        :param text_splitter: The text splitter object used for splitting the documents.
        :param process_func: The function to process each document.
        """
        if self.load_cache():
            return self.preprocessed_data

        print("Processing data...")
        for i in tqdm(range(len(self.data)), desc="Processing data", unit="chunk"):
            page_content = self.data[i]
            processed_chunk = process_func(text_splitter, page_content)
            self.preprocessed_data.extend(processed_chunk)
        
        self.save_cache()
        return self.preprocessed_data

    def perform_preprocessing(self, embeddings):
        """
        Perform preprocessing based on the selected text splitter type.
        
        :return: The preprocessed data.
        """
        if self.splitter_type == 'recursive':
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            return self.preprocess_data(text_splitter, lambda splitter, content: splitter.split_documents([content]))

        elif self.splitter_type == 'semantic':
            # breakpoint_percentile_threshold = 80
            text_splitter = SemanticChunker(embeddings=embeddings, breakpoint_threshold_type='standard_deviation', breakpoint_threshold_amount=2.0)
            all_chunk_documents = self.preprocess_data(text_splitter, lambda splitter, content: splitter.create_documents([content.page_content],  metadatas=[content.metadata])) # List[Document]
            for i,doc in enumerate(all_chunk_documents):
                doc.metadata['chunk_id'] = i
            return all_chunk_documents # with id for each chunk
        else:
            raise NotImplementedError(f"The splitter type '{self.splitter_type}' is not implemented.")




# if __name__ == '__main__':
#     load_dotenv()
#     from smart_companion.slconfig import SLConfig
#     from smart_companion.data_parser import DataParser
#     from smart_companion.config import config
#     from smart_companion.data_preprocessing import DataPreprocessor
    
#     cfg = config.combine_cfgs("/scratch/pranoy/heathrow_eval/results_and_eval/configs/experiment_vanilla_RAG.yaml")
#     # print(cfg['preprocessing_details']['chunk_size'])
    
    
#     dp = DataParser("https://lilianweng.github.io/posts/2023-06-23-agent/")
#     parsed_docs = dp.perform_parsing()
#     dpp = DataPreprocessor(parsed_docs[0],cfg=cfg)
#     pre_processed = dpp.perform_preprocessing()
#     print(pre_processed[0].metadata)

import time, os, re
from functools import wraps
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def generate_unique_name(cfg,file_name):
    final_name = file_name

    final_name += ("_embedding_type="+cfg["preprocessing_details"]["embedding_model"])

    if cfg["preprocessing_details"]["text_splitter"] == 'recursive':
        final_name += ("_chunk_strategy="+cfg["preprocessing_details"]["text_splitter"])
        final_name += ("_chunksize="+str(cfg["preprocessing_details"]["chunk_size"]))
        final_name += ("_overlap="+str(cfg["preprocessing_details"]["chunk_overlap"]))
    else:
        final_name += ("_"+cfg["preprocessing_details"]["text_splitter"])
    
    return final_name



def time_it(return_time=False):
    """Decorator to calculate the time taken by a function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()  # Start the timer
            result = func(*args, **kwargs)
            end_time = time.time()    # End the timer
            duration = end_time - start_time
            
            if return_time:
                print(f"Function '{func.__name__}' took {duration:.6f} seconds to execute.")
                return result, duration  # Return result and time taken
            else:
                print(f"Function '{func.__name__}' took {duration:.6f} seconds to execute.")
                return result
        return wrapper
    return decorator


def get_embedding_model(cfg):

    embedding_model_type = cfg["preprocessing_details"]["embedding_model"]

    if(embedding_model_type=="gemini"):
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    elif(embedding_model_type=="spacy"):
        embedding_model = SpacyEmbeddings(model_name="en_core_web_sm") 

    elif(embedding_model_type == "azure"):
        api_key = os.getenv("AZURE_EMBED_KEY")
        # embedding_model = AzureOpenAIEmbeddings(
        #         azure_deployment=cfg["preprocessing_details"]["azure_deployment"],
        #         openai_api_version=cfg["preprocessing_details"]["azure_api_version"],
        #         azure_endpoint=cfg["preprocessing_details"]["azure_endpoint"],
        #         api_key = api_key,
        #         model=cfg["preprocessing_details"]["azure_model"]
        #     )
        embedding_model = AzureOpenAIEmbeddings(
                    azure_deployment="ada_002_embedding_model",
                    openai_api_version="2023-03-15-preview",
                    azure_endpoint="https://nellllmkg-openai-instance-eastus.openai.azure.com/",
                    api_key = "a1a22c9153aa4418b92f65255f9aceb7",
                    model="text-embedding-ada-002"
                )
    return embedding_model

def extract_urls(text):
    url_pattern = r'URL Source:\s*(https?://\S+)'
    urls = re.findall(url_pattern, text)
    return urls if urls else ["No URLs found"]

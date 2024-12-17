from langchain_openai import AzureOpenAIEmbeddings
# from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embedding_model(cfg):

    embedding_model_type = cfg["preprocessing_details"]["embedding_model"]

    if(embedding_model_type=="gemini"):
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # elif(embedding_model_type=="spacy"):
    #     embedding_model = SpacyEmbeddings(model_name="en_core_web_sm") 

    elif(embedding_model_type == "azure"):
        api_key = os.getenv("AZURE_API_KEY")
        embedding_model = AzureOpenAIEmbeddings(
                azure_deployment=cfg["preprocessing_details"]["azure_deployment"],
                openai_api_version=cfg["preprocessing_details"]["azure_api_version"],
                azure_endpoint=cfg["preprocessing_details"]["azure_endpoint"],
                api_key = api_key,
                model=cfg["preprocessing_details"]["azure_model"]
            )
    return embedding_model
import os
from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import ChatCohere


class build_LLM:
    '''
    This class initializes openai, groq and gemini LLMs by just a single line of code, and provides a common API.
    '''
    def __init__(self,cfg,temperature=0) -> None:
        self.model_service_provider = cfg["model_service_provider"]
        self.model_name = cfg["model_name"]
        self.cfg = cfg
        self.llm = None
        self.api_key = None
        self.temperature = temperature
        

    def develop_llm(self):
        '''
        This function returns an LLM object which adhere to the api naming convention of langchain (llm.invoke(), llm.ainvoke(), llm.stream etc)
        '''
        if self.model_service_provider == "groq":
            return ChatGroq(model=self.model_name,temperature=0)
        
        elif self.model_service_provider == "google":
            
            return ChatGoogleGenerativeAI(model=self.model_name,temperature=0)
        
        elif self.model_service_provider == "azure":
            self.api_key = os.getenv("AZURE_API_KEY")
            return AzureChatOpenAI(
                    temperature=0,
                    api_key=self.api_key,  # Replace with your actual API key
                    api_version=self.cfg["api_version"],
                    azure_endpoint=self.cfg["azure_endpoint"],
                    model_name=self.cfg["model_name"]
                )
        elif self.model_service_provider == "cohere":
            self.api_key = os.getenv("COHERE_API_KEY")
            return ChatCohere(cohere_api_key="z9dBZyzularahz9lh2rnFhMVpTq2hagCnY2nZOuO",
                            model="command-r-plus-04-2024")
        else:
            raise ValueError(f"Unsupported LLM type: {self.model_name}")
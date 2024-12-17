from yacs.config import CfgNode as ConfigurationNode

# YACS overwrite these settings using YAML
__C = ConfigurationNode()

#cache_dir_information
__C.cache_information = ConfigurationNode()
__C.cache_information.cache_folder_location = "/mnt/home-ldap/parth_ldap/gen_ai/New_gala/gala_fj/src/gala_fj/cache_files"
__C.cache_information.cache_folder_path_for_file = None



#rag model details
__C.rag_model_details = ConfigurationNode()
__C.rag_model_details.model_service_provider = "cohere"
__C.rag_model_details.model_name =  "command-r-plus-04-2024" 

__C.rag_model_details.api_version = None
__C.rag_model_details.azure_deployment_name=None
__C.rag_model_details.azure_endpoint=None 
__C.rag_model_details.supported_models = []

#code model details
__C.code_model_details = ConfigurationNode()
__C.code_model_details.model_service_provider = "groq"
__C.code_model_details.model_name = "llama3-70b-8192"
__C.code_model_details.api_version = None
__C.code_model_details.azure_deployment_name=None
__C.code_model_details.azure_endpoint=None 
__C.code_model_details.supported_models = []


# router model details
__C.router_model_details = ConfigurationNode()
__C.router_model_details.model_service_provider = "groq"
__C.router_model_details.model_name = "llama3-70b-8192"
__C.router_model_details.api_version = None
__C.router_model_details.azure_deployment_name=None
__C.router_model_details.azure_endpoint=None 
__C.router_model_details.supported_models = []



#Database details
__C.graph_database_details = ConfigurationNode()
__C.graph_database_details.neo4j_user_name = None
__C.graph_database_details.neo4j_password = None
__C.graph_database_details.neo4j_uri = None
__C.sql_database_details = ConfigurationNode()
__C.sql_database_details.dbname = None
__C.sql_database_details.user = None
__C.sql_database_details.password = None
__C.sql_database_details.host = None
__C.sql_database_details.port = None

#preprocessing_details
__C.preprocessing_details = ConfigurationNode()
__C.preprocessing_details.chunk_size = 1000
__C.preprocessing_details.chunk_overlap = 200
__C.preprocessing_details.embedding_model = "spacy"
__C.preprocessing_details.text_splitter = "recursive" #can be semantic as well
__C.preprocessing_details.azure_endpoint= "https://nellllmkg-openai-instance-eastus.openai.azure.com/"
__C.preprocessing_details.azure_api_version= "2023-03-15-preview"
__C.preprocessing_details.azure_deployment= "ada_002_embedding_model"
__C.preprocessing_details.azure_model= "text-embedding-ada-002"

#retrieval_chain_details
__C.retrieval_chain_details = ConfigurationNode()
__C.retrieval_chain_details.dynamic = True
__C.retrieval_chain_details.static = True
__C.retrieval_chain_details.static_combined = None
__C.retrieval_chain_details.retrieve_relevant_questions = False
__C.retrieval_chain_details.retrieve_from_departures = True
__C.retrieval_chain_details.retrieve_from_arrivals = False

    
#retriever_details
__C.retriever_details = ConfigurationNode()
__C.retriever_details.topk = 6
__C.retriever_details.type = "simple"

__C.retriever_details.sparse_search = ConfigurationNode()
__C.retriever_details.sparse_search.perform_search = True
__C.retriever_details.sparse_search.search_method = "bm25"
__C.retriever_details.semantic_search = ConfigurationNode()
__C.retriever_details.semantic_search.perform_search = True
__C.retriever_details.semantic_search.search_method = "similarity"
__C.retriever_details.multiquery_search = ConfigurationNode()
__C.retriever_details.multiquery_search.perform_search = True
__C.retriever_details.kg_search = ConfigurationNode()
__C.retriever_details.kg_search.complete_kg = True
__C.retriever_details.kg_search.semantic_kg = True

__C.rag_chain_details = ConfigurationNode()
__C.rag_chain_details.chain_type = "simple chain"

    
__C.vqa = ConfigurationNode()
__C.vqa.use = False
__C.vqa.multimodal_retriever_name = "vidore/colpali"
__C.vqa.multimodal_retriever_path = "/scratch/models_hf/"
__C.vqa.multimodal_retriever_gpu_device = "cuda:0"
__C.vqa.vlm_name = "gemini-1.5-pro"
__C.vqa.vlm_service_provider = "google"
__C.vqa.pdf_folder = "/scratch/pranoy/cache/menu_pdfs"
__C.vqa.cache_file = "/scratch/pranoy/cache/pdf_image_cache.pkl"
__C.vqa.multimodal_retriever_top_n = 1 
__C.vqa.url_list_file = ""
    



models_compatable = {'gorq':["llama3-70b-8192","llama3-7b-8192"],
                     'google':["gemini-1.5-pro"],
                     'azure':["GPT-4 Turbo", "gpt-4o","gpt-4o-mini","GPT-4o (Omni)" ],
                     "cohere": ["command-r-plus-04-2024" ]}

def get_cfg_defaults():
    """
    Get a yacs CfgNode object with default values
    """
    # Return a clone so that the defaults will not be altered
    # It will be subsequently overwritten with local YAML.
    return __C.clone()

def combine_cfgs(cfg_path):
    # Priority 3: get default configs
    cfg_base = get_cfg_defaults()    

    # Priority 2: merge from yaml config
    if cfg_path is not None:
        cfg_base.merge_from_file(cfg_path)

    llm_type = ["rag_", "code_", "router_"]

    for type in llm_type:
        if cfg_base[type+"model_details"]["model_service_provider"] in models_compatable.keys():
            cfg_base[type+"model_details"]["supported_models"] = models_compatable[cfg_base[type+"model_details"]["model_service_provider"]]

            if cfg_base[type+"model_details"]["model_name"] not in cfg_base[type+"model_details"]["supported_models"]:
                print("please select a vald model from the selected provider")
                print("Available models are")
                print(cfg_base[type+"model_details"]["supported_models"])
                raise ValueError("Unsupported LLM type")

    return cfg_base

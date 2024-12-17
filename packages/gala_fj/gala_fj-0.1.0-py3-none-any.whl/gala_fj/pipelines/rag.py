import os
from concurrent.futures import ThreadPoolExecutor
import sys
# third part imports
from langchain import hub
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from dotenv import load_dotenv
import numpy as np
from langchain.retrievers import BM25Retriever
from langchain.schema import Document

# local imports
from gala_fj.data.processing.parser import DataParser
from gala_fj.data.processing.preprocessing import DataPreprocessor
from gala_fj.data.processing.storage import DataStorage
from gala_fj.retrievers.hybrid_retriever import DataRetriever
from gala_fj.llms.llm import build_LLM
from gala_fj.flow.retrieval_chains import RetrievalChains
from gala_fj.config import config
from gala_fj.utils.additional_functionalities import generate_unique_name,get_embedding_model
# from smart_companion.dynamic_data_manipulation.database_RAG import DB_RAG
from gala_fj.prompts.prompts import Prompts,query_router_prompts
# from smart_companion.pdf_analysis.colpali_with_vlm import PDFAnalyzer
# from smart_companion.dynamic_data_manipulation.fetch_train_and_rail_status import format_status_output, heathrow_rail_and_tube_info_dict




load_dotenv()

class RAG():
    '''
    Main class for orchestrating the entire Retrieval Augmented Generation pipeline
    '''
    def __init__(self,data_source,cfg,history_aware = None):
        self.cfg = cfg
        self.data_source = data_source
        self.retriever = None
        self.prompt = None
        self.query_type = None
        self.use_dynamic_data = cfg['retrieval_chain_details']['dynamic']
        self.use_static_data = cfg['retrieval_chain_details']['static']
        # separate llm definitions for different sub-tasks
        # self.llm_text2sql = build_LLM(cfg=cfg["code_model_details"]).develop_llm()
        self.llm_router = build_LLM(cfg=cfg["router_model_details"]).develop_llm()
        self.llm_rag = build_LLM(cfg=cfg["rag_model_details"]).develop_llm()
        self.embedding_model= get_embedding_model(cfg)
        self.perform_initial_setup(cfg)
        self.answer = None
        self.history_aware = history_aware
        self.question = None
        self.chat_history = []
        self.retrieve_relevant_questions = cfg['retrieval_chain_details']['retrieve_relevant_questions']
        self.bm25_retriever = None
        self.topk = 4  # Number of relevant history items to retrieve
        self.citation_prompt = """While answering the question, ALWAYS cite the contexts with the reference numbers, in the format [citation:x] if they are NECESSARY TO ANSWER THE QUESTION. If a sentence comes from multiple contexts, please list all applicable citations, like [citation:3][citation:5]. 
                                Other than code and specific names and citations, your answer must be written in the same language as the question.

                                NEVER FORGET TO PROVIDE THE CORRECT CITATIONS
                                """

    def perform_initial_setup(self,cfg):
        '''
        To be written
        '''
        
        data_parser = DataParser()
        parsed_data,input_file_name = data_parser.perform_parsing(self.data_source)
        unique_identifier = generate_unique_name(cfg,input_file_name)

        cfg["cache_information"]["cache_folder_path_for_file"] = os.path.join(cfg["cache_information"]["cache_folder_location"],unique_identifier)

        if not os.path.exists(cfg["cache_information"]["cache_folder_path_for_file"]):
            os.mkdir(cfg["cache_information"]["cache_folder_path_for_file"])

        #print("Finished exporting the Data")
        
        data_preprocessing = DataPreprocessor(parsed_data,cfg=cfg)
        data_chunks = data_preprocessing.perform_preprocessing(self.embedding_model)
        self.data_chunks = data_chunks
        #print("Finished chunking the Data")
        
    
        data_source = DataStorage(data_chunks,cfg=cfg).perform_storage(self.embedding_model)
        #print("Finished storage of the Data")

        self.retriever = DataRetriever(cfg=cfg,llm=self.llm_rag,preprocessed_data=data_chunks,vector_store=data_source).generate_retriever()
        # self.prompt = hub.pull("rlm/rag-prompt")
        self.prompt = PromptTemplate(
                        input_variables=['context', 'question'],
                        template=(
                            "You are an assistant for reading comprehesion tasks."
                            "Look carefully through all the pieces of retrieved context provided to answer the question. "
                            "If you don't know the answer, just say that you don't know. "
                            # "ALWAYS ANSWER IN ENGLISH and use three sentences maximum and keep the answer concise.\n"
                            """While answering the question, ALWAYS CITE THE CONTEXTS WITH THE REFERENCE NUMBERS, in the format [citation:x] if they are NECESSARY TO ANSWER THE QUESTION. If a sentence comes from multiple contexts, please list all applicable citations, like [citation:3][citation:5]. 
                               Other than code and specific names and citations, your answer must be written in the same language as the question.
                               NEVER FORGET TO PROVIDE THE CORRECT CITATIONS"""
                            "ALWAYS ANSWER IN ENGLISH and dont say 'according to the provided context' as you are a comapanion to a human - imagine what kind of response a human would find useful "
                            " and IF THERE IS AMBIGUITY ALWAYS GIVE ALL PLAUSIBLE ANSWERS FROM THE PROVIDED CONTEXT ONLY\n"
                            "Question: {question} \nContext: {context} \nAnswer:"
                            "Your generated answer is going to be displayed in a markdown friendly environment - SO GIVE WELL FORMATTED MARKDOWN TEXT AND USE LISTS WHENEVER NECESSARY"
                        )
                    )
        
        self.final_qa_chain = self.prompt | self.llm_rag

        # k  = self.final_qa_chain.
        
        if self.use_dynamic_data is True:
            self.dynamic_data_retrieval_chain = DB_RAG(cfg = cfg,llm = self.llm_text2sql).retriever
        else: self.dynamic_data_retrieval_chain = None

        if self.use_static_data is True:
            self.static_data_retrieval_chain = RetrievalChains(chain_type=cfg["rag_chain_details"]["chain_type"],
                                                            prompt=self.prompt,
                                                            retriever=self.retriever,
                                                            llm=self.llm_rag,
                                                            cfg=cfg)
        else:
            self.static_data_retrieval_chain = None

        if self.use_dynamic_data is None and self.use_static_data is None:
            #print("Atleast one of the retrieval chains (static or dynamic) has to be switched on in the config file")
            sys.exit()
            
        if self.cfg['vqa']['use']:
            # Initialize PDFAnalyzer
            self.pdf_analyzer = PDFAnalyzer(self.cfg)
        
    def query_router(self, query):
        '''
        This function invokes an LLM to predict the type of the query - restaurant or normal
        '''
        examples= query_router_prompts().examples
        example_prompt_template = PromptTemplate(
                                    input_variables=["question", "output"],
                                    template="""
                                    Example:
                                    Question: "{question}"
                                    Expected Output: {output}
                                    """)

        few_shot_prefix = query_router_prompts().few_shot_prefix

        few_shot_prompt_template = FewShotPromptTemplate(
                                            examples=examples,
                                            example_prompt=example_prompt_template,
                                            prefix=few_shot_prefix,
                                            suffix=""" Question: "{question}"
                                            Your output should be `True` for restaurant menu specific questions and `False` otherwise.
                                            """,
                                            input_variables=["question"]
                                        )
        formatted_prompt = few_shot_prompt_template.format(question=query)
        output = self.llm_router.invoke(formatted_prompt).content
        if "true" in output.lower():
            return "Restaurant"
        else: return "Normal"
            
    def get_combined_context(self, query: str, static_data_retrieval_chain,\
        dynamic_data_retrieval_chain = None):
        '''
        Function that calls different data source modules to create the aggregated context for ultimate LLM call
        ''' 

        # Function to call module's find_answer
        def get_response_dynamic(dynamic_data_retrieval_chain):
            return str(dynamic_data_retrieval_chain(query))
        
        def get_response_static(static_data_retrieval_chain):
            if self.cfg['retrieval_chain_details']['static_combined']:
                query_type="combined"
            else: query_type = self.query_router(query)
            
            if query_type=="factoid":
                return static_data_retrieval_chain.stratified_kg_sampler(query)
            elif(query_type=="descriptive"): # descriptive
                
                return static_data_retrieval_chain.only_retriever(query,self.chat_history)
            else:
                # #print("Invoking both SemKG and Hybrid RAG ...")
                return static_data_retrieval_chain.hybrid_retriever(query,self.chat_history)

        if dynamic_data_retrieval_chain is not None and static_data_retrieval_chain is not None:
            # Use ThreadPoolExecutor to run module calls in parallel
            with ThreadPoolExecutor() as executor:
                # Submit tasks to the thread pool
                futures = [
                    executor.submit(get_response_dynamic, dynamic_data_retrieval_chain),
                    executor.submit(get_response_static, static_data_retrieval_chain),
                    executor.submit(get_response_tube_and_rail),
                ]
                
                # Wait for all futures to complete and gather results
                results = [future.result() for future in futures]

            # Combine the results (concatenation)
            combined_context = " ".join(results)
        elif dynamic_data_retrieval_chain is not None:
            combined_context = get_response_dynamic(dynamic_data_retrieval_chain)
        else:
            combined_context = get_response_static(static_data_retrieval_chain)
        return combined_context
    
    def update_bm25_retriever(self):
        if not self.chat_history:
            self.bm25_retriever = None
            return
        
        documents = [
            Document(
                page_content=f"Question: {qa[0]}\nAnswer: {qa[1]}",
                metadata={"index": i}
            )
            for i, qa in enumerate(self.chat_history)
        ]
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = self.topk
        
    def get_relevant_history(self, question):
        if not self.bm25_retriever:
            return []
        
        relevant_docs = self.bm25_retriever.get_relevant_documents(question)
        relevant_history = [
            self.chat_history[doc.metadata["index"]]
            for doc in relevant_docs
        ]
        return relevant_history
    
    def rephrase_query(self, prompt_template, context, question):
        prompt = prompt_template.format(context=context, question=question)
        rephrased_question = self.llm_rag.invoke(prompt).content
        return rephrased_question.strip()
    
    def manage_chat_history(self, question, answer):
        # doc = 
        self.chat_history.append((question, answer))
        if len(self.chat_history) > 5:  # Keep only the last 5 exchanges
            self.chat_history = self.chat_history[-5:]
        self.update_bm25_retriever()
        
    # def format_chat_history(self, chat_history):
    #     formatted_history = ""
    #     for i, (question, answer) in enumerate(chat_history, 1):
    #         formatted_history += f"Exchange {i}:\n"
    #         formatted_history += f"Human: {question}\n"
    #         formatted_history += f"AI: {answer}\n\n"
    #     return formatted_history.strip()
    

    def format_chat_history(self,chat_history):
        formatted_history = ""
        for i, (question, answer) in enumerate(chat_history, 1):
            formatted_history += f"Question/Answer {i}:\n"
            formatted_history += f"Question: {question}\n"
            formatted_history += f"Answer: {answer}\n\n"
        return formatted_history.strip()
    
    def find_answer_with_source(self,question):
        '''
        Fetches the combined context and invokes an LLM to generate an answer corresponding to the question and context.
        '''
        #Rephrase the question based on the history question and answer summary
        if self.history_aware and len(self.chat_history)>0:
            relevant_history = self.chat_history
            if(self.retrieve_relevant_questions):
                relevant_history = self.get_relevant_history(question)
            # #print(relevant_history)
            formatted_history = self.format_chat_history(relevant_history)
            rephrased_question = self.rephrase_query(Prompts().prompt, formatted_history, question)
            #print("Rephrased question is: ",rephrased_question)
        else:
            rephrased_question = question
            relevant_history = []
        # combined_context = self.get_combined_context(
        #         query=rephrased_question,
        #         static_data_retrieval_chain=self.static_data_retrieval_chain,
        #         dynamic_data_retrieval_chain=self.dynamic_data_retrieval_chain
        #     )

        combined_context = self.get_combined_context(
                query=rephrased_question,
                static_data_retrieval_chain=self.static_data_retrieval_chain,
            )

        # #print("Combined Context is: ",combined_context)
        # self.answer = self.llm.invoke(self.prompt.invoke({
        #     "context": combined_context,
        #     "question": question,
        #     "chat_history": relevant_history
        # })).content
        
        self.answer = self.final_qa_chain.invoke({
            "context": combined_context,
            "question": question,
            "chat_history": relevant_history
        }).content
        
        if self.history_aware:
            self.manage_chat_history(question, self.answer)
            
        return self.answer

    def pdf_visual_qa(self,query):
        '''
        colpali
        This function returns a stream generator for token by token generation
        '''

        #print("Question for pdf retriever")
        #print("$"*40)
        #print(query)
        #print("$"*40)
        return self.pdf_analyzer.analyze_stream(query)
    
    def get_static_dynamic_qa(self,question):
        '''
        Fetches the combined context and invokes an LLM to generate an answer corresponding to the question and context.
        This function returns a stream generator for token by token generation
        '''

        combined_context = self.get_combined_context(
                query=question,
                static_data_retrieval_chain=self.static_data_retrieval_chain,
                dynamic_data_retrieval_chain=self.dynamic_data_retrieval_chain
            )
        # with open("input_context_all_files.txt", "w") as file:
        #     # Write the string to the file
        #     file.write(combined_context)
                
        return self.final_qa_chain.stream({
            "context": combined_context,
            "question": question,
            # "chat_history": relevant_history
        })
    
    def get_stream_generator(self, question):
        '''
        This function routes the query to either pdf_visual_qa method or static_dynamic_qa method
        '''

        #Rephrase the question based on the history question and answer summary
        if self.history_aware:
            relevant_history = self.chat_history
            if(self.retrieve_relevant_questions):
                relevant_history = self.get_relevant_history(question)
            # #print(relevant_history)
            formatted_history = self.format_chat_history(relevant_history)
            ##print("This is fomatted history-------------------------------------------\n\n\n")
            #print(formatted_history)
            rephrased_question = self.rephrase_query(Prompts().prompt, formatted_history, question)
            #print("This is rephrased question-----------------------------------------\n\n")
            #print(rephrased_question)
        else:
            rephrased_question = question
            relevant_history = []

        question = rephrased_question
        if self.cfg['vqa']['use'] is False:
            return self.get_static_dynamic_qa(rephrased_question)
        else:
            # understand type of query
            self.query_type = self.query_router(rephrased_question)
            if self.query_type == "Restaurant":
                # #print("Restaurant related query ...")
                #print("pdf retrival is working!!!")
                return self.pdf_visual_qa(rephrased_question)
            else:
                # #print("Query not related to restaurant ...")
                #print("semantic retrival is working!!!")
                return self.get_static_dynamic_qa(rephrased_question)
            
            
        

if __name__ == '__main__':
    
    cfg = config.combine_cfgs("/mnt/home-ldap/parth_ldap/gen_ai/New_gala/gala_fj/config.yaml")
    load_dotenv()

    #creating cache_dir
    if not os.path.exists(cfg["cache_information"]["cache_folder_location"]):
        os.mkdir(cfg["cache_information"]["cache_folder_location"])

    # rg = RAG("https://lilianweng.github.io/posts/2023-06-23-agent/",cfg)
    # #print(rg.find_answer_with_source("What is Task Decomposition?"))
    
    # #"What is the Terms and Conditions of Heathrow Rewards?"
    rg = RAG("/mnt/home-ldap/parth_ldap/gen_ai/attn_is_all_you_need.pdf",cfg)
    print(rg.find_answer_with_source("What is the blue score for transformer in table 2 for EN-FR"))

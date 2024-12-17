import concurrent.futures

from neo4j import GraphDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

# from gala.src.gala.prompts.prompts import Prompts,query_router_prompts


class RetrievalChains():
    '''
    This class implements different retrieval paths from different data sources
    '''
    def format_chat_history(self,chat_history):
        formatted_history = ""
        for i, (question, answer) in enumerate(chat_history, 1):
            formatted_history += f"Question/Answer {i}:\n"
            formatted_history += f"Question: {question}\n"
            formatted_history += f"Answer: {answer}\n\n"
        return formatted_history.strip()
    
    def __init__(self,chain_type,prompt,retriever,llm,cfg):
        
        self.chain_type = chain_type
        self.prompt = prompt
        self.retriever = retriever
        self.llm = llm
        self.entity_llm = llm
        self.generated_rag_chain = None
        username = cfg["graph_database_details"]["neo4j_user_name"]
        password = cfg["graph_database_details"]["neo4j_password"]
        uri      = cfg["graph_database_details"]["neo4j_uri"]
        self.neo4j_driver = GraphDatabase.driver(uri, auth=(username, password))
        self.retrieved_documents = None
        self.kg = []
        self.setup_history_aware_retrieval()
        
    def setup_history_aware_retrieval(self):
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("human", "latest Question: {input}"),
            ("human","Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question by using answers to the previous questions which can be understood without the chat history. Do NOT answer the question,just reformulate it based on previous Question and Answers if needed and otherwise return it as is chat History:{chat_history}")
        ])

        self.history_aware_retriever = create_history_aware_retriever(
            llm=self.llm,
            retriever=self.retriever,
            prompt=self.contextualize_q_prompt
        )

        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the user's question based on the following context:\n\n{context}, Use this chat history for the reference, chat_history:{chat_history}"),
            # ("chat_history", "Use this chat history for the reference, chat_history:{chat_history}"),
            # MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)
        self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.question_answer_chain)


    def _format_docs(self,docs):
        # print("---------------------------------")
        # print(docs[0].metadata.get('id'))
        # print("---------------------------------")
        return "\n\n".join(doc.page_content for doc in docs)

    def get_triples_with_entities(self, entities):
        '''
        Invoke Neo4j graph db session to execute cypher query for 
        retrieving subject-relation-object triples based on 
        the given "entities"
        '''
        # Preprocess entities to handle various input variations
        processed_entities = []
        for entity in entities:
            # Convert to lowercase and strip whitespace
            cleaned_entity = entity.lower().strip()
            # Remove any extra whitespace within the entity
            cleaned_entity = ' '.join(cleaned_entity.split())
            processed_entities.append(cleaned_entity)

        # print("PROCESSED ENTITIES ", processed_entities)
        
        try:
            with self.neo4j_driver.session() as session:
                # Update the query to use UNWIND for multiple entities
                # and perform case-insensitive partial matching with more flexibility
                query = """
                UNWIND $entities AS entity
                MATCH (a)-[r]->(b)
                WHERE 
                    // Case-insensitive partial match with word boundary considerations
                    toLower(a.name) CONTAINS entity OR 
                    toLower(a.name) =~ '(?i).*\\b' + entity + '\\b.*'
                RETURN DISTINCT a.name AS subject, type(r) AS relation, b.name AS object
                LIMIT 700
                """
                
                # Run the query
                result = session.run(query, entities=processed_entities)
                
                # Collect triples
                triples = []
                for record in result:
                    subject = record['subject']
                    relation = record['relation']
                    object_ = record['object']
                    
                    # Append to triples list as a dictionary
                    triples.append({
                        "subject": subject, 
                        "relation": relation, 
                        "object": object_
                    })
                
                return triples

        except Exception as e:
            print(f"❌ Triple extraction failed: {e}")
            return []

    def get_triples_with_entities_labelwise(self, entities, label):
        '''
        Invoke Neo4j graph db session to execute cypher query for 
        doing a 1-hop traversal of the "label" indexed sub-KG based.
        Traversal starts with the given "entities"
        '''
        # print(label)
        # Preprocess entities to handle various input variations
        processed_entities = []
        for entity in entities:
            # Convert to lowercase and strip whitespace
            cleaned_entity = entity.lower().strip()
            # Remove any extra whitespace within the entity
            cleaned_entity = ' '.join(cleaned_entity.split())
            processed_entities.append(cleaned_entity)

        print("PROCESSED ENTITIES ", processed_entities)

        try:
            with self.neo4j_driver.session() as session:
                # Sanitize the label
                sanitized_label = f"Label_{label}"

                # Define the query with more flexible matching
                query = (
                    f"""
                    UNWIND $entities AS entity
                    MATCH (s:{sanitized_label})-[r]->(o:{sanitized_label})
                    WHERE 
                        toLower(s.name) CONTAINS entity OR 
                        toLower(s.name) =~ '(?i).*\\b' + entity + '\\b.*' OR
                        toLower(o.name) CONTAINS entity OR 
                        toLower(o.name) =~ '(?i).*\\b' + entity + '\\b.*'
                    RETURN DISTINCT s.name AS subject, type(r) AS relation, o.name AS object
                    LIMIT 70
                    """
                )

                result = session.run(query, entities=processed_entities)
                
                # Collect results
                triples = []
                for record in result:
                    triples.append({
                        "subject": record["subject"], 
                        "relation": record["relation"], 
                        "object": record["object"]
                    })

                # If you want to output as a CSV-like string
                triples_str = "\n".join([f"{triple['subject']},{triple['relation']},{triple['object']}" for triple in triples])
                
                return triples, triples_str

        except Exception as e:
            print(f"❌ Triple extraction failed: {e}")
            return [], ""

    def retrieve_from_neo4j(self, cypher_query):
        '''
        Invoke Neo4j graph db session to execute a cypher query
        '''
        if not cypher_query:
            return []
        with self.neo4j_driver.session() as session:
            result = session.run(cypher_query)
            return [record['n'] for record in result]
    
    def extract_entities(self,text):
        '''
        invoke an LLM to extract named entities from given natural language text
        '''
        # Define your few-shot examples
        few_shot_examples = (
            "Extract the entities from the following text:\n"
            "Text: \"The Eiffel Tower is located in Paris.\"\n"
            "Entities:\n"
            "Eiffel Tower\n"
            "Paris\n\n"
            "Extract the entities from the following text:\n"
            "Text: \"Apple Inc. was founded by Steve Jobs in Cupertino.\"\n"
            "Entities:\n"
            "Apple Inc\n"
            "Steve Jobs\n"
            "Cupertino\n\n"

            "STRICTLY follow the output format: entity1,entity2,entity3,..."
        )
        
        # Create the prompt
        prompt = f"{few_shot_examples}Extract the entities from the following text:\nText: \"{text}\"\nEntities:"
        
        # Query the model
        response = self.entity_llm.predict(prompt)
        # print("RESPONSE ",response)
        return response.split(",")

    def kg_sampler(self, question):
        # Retrieve KG triples
        entities = self.extract_entities(question)
        # entities = entities.splitlines()
        kg_triples = self.get_triples_with_entities(entities)
        # print("KG EXTRACTED ",kg_triples)
        return "\n".join([f"{triple['subject']} -[{triple['relation']}]-> {triple['object']}" for triple in kg_triples])
    
    def stratified_kg_sampler(self,question):
        relevant_docs = self.retriever.get_relevant_documents(question)
        relevant_ids = []
        for docs in relevant_docs:
            relevant_ids.append(docs.metadata['chunk_id'])
        # print("-----------------------------------------------")
        # print("Relevant chunk ids are ",relevant_ids)
        # print("-----------------------------------------------")
        entities = self.extract_entities(question)
        kg_context = []
        for idx in relevant_ids:
            # Fetch single-hop triples
            kg_triples, _ = self.get_triples_with_entities_labelwise(entities, idx)
            # print("KG EXTRACTED ",kg_triples)
            # print(f"For idx {idx}, KG LABEL WISE {kg_triples}")
            kg_context.append("\n".join([f"{triple['subject']} -[{triple['relation']}]-> {triple['object']}" for triple in kg_triples]))
            self.kg.append(kg_triples)
        
        # print("Final KG ",kg_context)
        return '\n '.join(kg_context)
    
    # def only_retriever(self,query):
    #     return self._format_docs(self.retriever.get_relevant_documents(query))
    
    def retrieve_with_history(self, query, chat_history):
        # print("chat history: ",chat_history)
        # Prompts_obj = Prompts()
        formatted_history = self.format_chat_history(chat_history)
        # print("Formatted History", type(formatted_history))
        result = self.rag_chain.invoke({
            "input": query,  # Changed from "question" to "input"
            "chat_history": formatted_history
        })
        return result["answer"]


    def only_retriever(self, query, chat_history=None):
        # print("Chat Hostory: ",chat_history)
        if chat_history:
            return self.retrieve_with_history(query, chat_history)
        else:
            self.retrieved_documents = self.retriever.get_relevant_documents(query)
            return self._format_docs(self.retrieved_documents)

    # def hybrid_retriever(self, query, chat_history=None):
    #     kg_context = self.stratified_kg_sampler(query)
    #     text_context = self.only_retriever(query, chat_history)
    #     return f"{text_context}\n\nKnowledge Graph Context:\n{kg_context}"
    
    def format_context_with_citation_number(self,list_of_docs,kg_context):
        output = ""
        citation_count = 1
        content = {"Knowledge Graph": ""}
        for document in list_of_docs:
            # TO DE FIXED
            if "url" not in document.metadata:
                continue
            if len(document.metadata["url"])==0:
                document.metadata["url"] = [" "]
                
            if document.metadata["url"][0].split("/")[-1] not in content:
                content[document.metadata["url"][0].split("/")[-1]] = ""
            content[document.metadata["url"][0].split("/")[-1]] += (
                f"{document.page_content}" + "\n"
            )

        # add all content to final output string
        output = f"[citation:0]: Knowledge Graph \n {kg_context} \n"
        for key in content.keys():
            output += f"--------------------------------------------------------------------------------- \n [citation: {citation_count}] \n \
                --------------------------------------------------------------------------------- \n  {key} \n {content[key]}"
            citation_count += 1

        return output

 
    def hybrid_retriever(self, query, chat_history=None):
        '''
        Returns the retrieved information from both the KG and hybridRAG
        '''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit both tasks to be run in parallel
            if self.chain_type == "simple":
                text_context_future = executor.submit(self.only_retriever, query, chat_history)
                text_context = text_context_future.result()

            elif self.chain_type == "kg": #simple,kg,sem_kg
                text_context_future = executor.submit(self.only_retriever, query, chat_history)
                kg_context_future = executor.submit(self.kg_sampler, query)
                kg_context = kg_context_future.result()
                text_context = text_context_future.result()
            
            elif self.chain_type == "sem_kg": #simple,kg,sem_kg
                text_context_future = executor.submit(self.only_retriever, query, chat_history)
                kg_context_future = executor.submit(self.stratified_kg_sampler, query)
                kg_context = kg_context_future.result()
                text_context = text_context_future.result()
            
            # Wait for the results of both tasks

        return self.format_context_with_citation_number(self.retrieved_documents,self.kg)
        #return f"{text_context}\n\nKnowledge Graph Context:\n{kg_context}"
        
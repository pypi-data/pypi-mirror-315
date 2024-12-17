import re
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage
from gala_fj.data.graphs.kg_insertion import Neo4jKnowledgeGraphHandler
import os

class TripleExtractor:
    def __init__(self,cfg,output_file="triples.txt"):
        """
        Initialize the TripleExtractor with an output file.

        Args:
            output_file (str): The file where extracted triples will be stored.
        """
        self.output_file = output_file
        self.cfg = cfg
        self.chain_type = cfg["rag_chain_details"]["chain_type"]
    
    def extract_and_save_triples(self,input_text, output_file="triples.txt",label=None):
        """
        Extract triples from text and save to a file.
        
        Args:
            input_text (str): Text containing triples
            output_file (str, optional): Output filename. Defaults to 'triples.txt'.
        """
        # Extract triples using regex
        # print("PATHHHH ",output_file)
        triples = re.findall(r'subject:\s*([^,]+),\s*relation:\s*([^,]+),\s*object:\s*(.+)', input_text)
        
        # Write triples to file
        with open(output_file, 'w', encoding='utf-8') as f:
            for subject, relation, obj in triples:
                # Clean and replace commas to avoid parsing issues
                clean_subject = subject.strip().replace(',', ';')
                clean_relation = relation.strip().replace(',', ';')
                clean_object = obj.strip().replace(',', ';')
                
                f.write(f"{clean_subject},{clean_relation},{clean_object}\n")
        
        print(f"Extracted {len(triples)} triples to {output_file}")
        # if self.chain_type == "kg":
        #     neo4j_handler = Neo4jKnowledgeGraphHandler(self.cfg["graph_database_details"]["neo4j_uri"],
        #                                     self.cfg["graph_database_details"]["neo4j_user_name"],
        #                                     self.cfg["graph_database_details"]["neo4j_password"])
        #     neo4j_handler.process_single_file(file_path=output_file)
        #     print("YAAHHHAAANnn")
        #     neo4j_handler.close()
        # elif self.chain_type == "sem_kg":
        #     neo4j_handler = Neo4jHandler_KG(self.cfg["graph_database_details"]["neo4j_user_name"],
        #                                     self.cfg["graph_database_details"]["neo4j_password"],
        #                                     self.cfg["graph_database_details"]["neo4j_uri"])
        #     neo4j_handler.process_single_file(output_file, neo4j_handler)
        #     neo4j_handler.close()

    def extract_triples(self, triple_text,output_path):
        self.api_key = os.getenv("AZURE_API_KEY")
        llm = AzureChatOpenAI(
                    temperature=0,
                    api_key=self.api_key,  # Replace with your actual API key
                    api_version=self.cfg["router_model_details"]["api_version"],
                    azure_endpoint=self.cfg["router_model_details"]["azure_endpoint"],
                    model_name=self.cfg["router_model_details"]["model_name"]
                )

        message = [
                SystemMessage(
                    content = (
                        """ 
                        Task: Comprehensively extract ALL the triples (subject, relation, object) from below given paragraph. Ensure that the subject and objects in the triples are named entities (name of person, organization, dates etc) and not multiple in number. You will be HEAVILY PENALIZED if you violate this constraint. 

                        Examples: Use the following examples to understand the task better. \n \
                        
                        paragraph: William Rast is an American clothing line founded by Justin Timberlake and Trace Ayala. 
                        It is most known for their premium jeans.  On October 17, 2006, Justin Timberlake and Trace Ayala put on their 
                        first fashion show to launch their new William Rast clothing line.  The label also produces other clothing items
                        such as jackets and tops.  The company started first as a denim line, later evolving into a men's and women's clothing line.

                        triples: 
                        (i) subject: William Rast, relation: clothing line, object: American
                        (ii) subject: William Rast, relation: founded by, object: Justin Timberlake
                        (iii) subject: William Rast, relation: founded by, object: Trace Ayala
                        (iv) subject: William Rast, relation: known for, object: premium jeans
                        (v) subject: William Rast, relation: launched on , object: October 17, 2006
                        (vi) subject: Justin Timberlake, relation: first fashion show, object: October 17, 2006
                        (vii) subject: Trace Ayala, relation: first fashion show, object: October 17, 2006
                        (viii) subject: William Rast, relation: produces, object: jackets
                        (ix) subject: William Rast, relation: produces, object: tops
                        (x) subject: William Rast, relation: started as, object: denim line
                        (xi) subject: William Rast, relation: evolved into, object: men's and women's clothing line


                        paragraph: The Glennwanis Hotel is a historic hotel in Glennville, Georgia, Tattnall County, Georgia,
                        built on the site of the Hughes Hotel.  The hotel is located at 209-215 East Barnard Street.  The old Hughes Hotel was 
                        built out of Georgia pine circa 1905 and burned in 1920.  The Glennwanis was built in brick in 1926.  The local Kiwanis 
                        club led the effort to get the replacement hotel built, and organized a Glennville Hotel Company with directors being 
                        local business leaders.  The wife of a local doctor won a naming contest with the name "Glennwanis Hotel", a suggestion
                        combining "Glennville" and "Kiwanis"

                        triples:
                        (i) subject: Glennwanis Hotel, relation: is located in, object: 209-215 East Barnard Street, Glennville, Tattnall County, Georgia
                        (ii) subject: Glennwanis Hotel, relation: was built on the site of, object: Hughes Hotel
                        (iii) subject: Hughes Hotel, relation: was built out of, object: Georgia pine
                        (iv) subject: Hughes Hotel, relation: was built circa, object: 1905
                        (v) subject: Hughes Hotel, relation: burned in, object: 1920
                        (vi) subject: Glennwanis Hotel, relation: was re-built in, object: 1926
                        (vii) subject: Glennwanis Hotel, relation: was re-built using, object: brick
                        (viii) subject: Kiwanis club, relation: led the effort to re-build, object: Glennwanis Hotel
                        (viii) subject: Kiwanis club, relation: organized, object: Glennville Hotel Company
                        (ix) subject: Glennville Hotel Company, relation: directors, object: local business leaders
                        (x) subject: Glennwanis Hotel, relation: combines, object: "Glennville" and "Kiwanis"


                        paragraph: Dr. Lisa K. Randall (June 18, 1962 - present) is an American theoretical physicist and\
                        a leading expert in particle physics and cosmology at Harvard University, located in Cambridge, \
                        Massachusetts. Her notable work includes research on dark matter and extra dimensions. Cambridge \
                        is part of Middlesex County, where she has made significant contributions to the scientific community.

                        Triples:
                        (i) subject: Dr. Lisa K. Randall, relation: was born on, object: June 18, 1962
                        (ii) subject: Dr. Lisa K. Randall, relation: expert in, object: particle physics and cosmology
                        (iii) subject: Dr. Lisa K. Randall, relation: works at, object: Harvard University
                        (iv) subject: Harvard University, relation: located in, object: Cambridge, Massachusetts
                        (v) subject: Cambridge, Massachusetts, relation: part of, object: Middlesex County
                        (vi) subject: Dr. Lisa K. Randall, relation: conducted research on, object: dark matter and extra dimensions
                        (vii) subject: Dr. Lisa K. Randall, relation: contributed to, object: scientific community in Middlesex County
                        
                        paragraph: John C. Petersen (November 2, 1842 - July 10, 1887) was an American butcher and farmer from \
                        Appleton, Wisconsin who served as a member of the Wisconsin State Assembly from Outagamie County.


                        Triples:
                        (i) subject: John C. Petersen, relation: born on, object: November 2, 1842
                        (ii) subject: John C. Petersen, relation: died on, object: July 10, 1887
                        (iii) subject: John C. Petersen, relation: occupation, object: American butcher and farmer
                        (iv) subject: John C. Petersen, relation: belongs to, object: Appleton, Wisconsin
                        (v) subject: John C. Petersen, relation: member of, object: Wisconsin State Assembly
                        (vi) subject: John C. Petersen, relation: represents, object: Outagamie County
                        (vi) subject: Appleton, Wisconsin, relation: located in, object: Outagamie County


                        *Output format strictly as follows:**
                        Triples:
                        (i) subject: [subject], relation: [relation], object: [object]
                        (ii) subject: [subject], relation: [relation], object: [object]
                        (iii) subject: [subject], relation: [relation], object: [object]
                        ...

                        **Note:** Do not deviate from this format. If any data is ambiguous or missing, clearly state "ambiguous" or "missing" for the respective field.
                        """
                    ),
                ),
                    HumanMessage(
                        content=[
                            {
                                "type": "text",
                                "text": triple_text
                            },
                        ]
                    )
                ]

        triple_text = llm.invoke(message).content
        self.extract_and_save_triples(triple_text,output_file=output_path)
        return triple_text


# Example usage
# if __name__ == "__main__":
#     triple_text = '''Triples:\n\n(i) subject: Docling, relation: is, object: open-source document conversion tool\n\n(ii) subject: Docling, relation: builds on, object: specialized AI models and datasets\n\n(iii) subject: Docling, relation: designed as, object: simple, self-contained python library\n\n(iv) subject: Docling, relation: runs on, object: commodity hardware\n\n(v) subject: Docling, relation: converts PDF documents to, object: JSON or Markdown format\n\n(vi) subject: Docling, relation: extracts, object: metadata\n\n(vii) subject: Docling, relation: recovers, object: table structures'''

#     # Create an object of TripleExtractor
#     extractor = TripleExtractor(output_file="docling_triples.txt")

#     # Extract and save triples
#     extracted_triples = extractor.extract_triples("obama is president of america")

#     # Print extracted triples
#     print("\nExtracted Triples:")
#     for triple in extracted_triples:
#         print(triple)

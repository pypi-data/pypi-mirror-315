import os
import re
import yaml
from typing import List, Tuple
from neo4j import GraphDatabase

class Neo4jKnowledgeGraphHandler:
    """
    A comprehensive handler for creating and managing knowledge graphs in Neo4j.
    Supports both labeled and unlabeled node creation with flexible configuration.
    """

    def __init__(self,uri,user_name,password):
        """
        Initialize the Neo4j handler with configuration from a YAML file.

        Args:
            config_path (str): Path to the configuration YAML file.
        """
        self.uri = uri
        self.username = user_name
        self.password = password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    
    def _load_config(self,config_path: str) -> dict:
        """
        Load configuration from a YAML file.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            dict: Loaded configuration dictionary.
        """
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except (IOError, yaml.YAMLError) as e:
            raise ValueError(f"Error loading configuration: {e}")

    def connect(self):
        """Establish a connection to the Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Neo4j: {e}")

    def close(self):
        """Close the Neo4j database connection."""
        if self.driver:
            self.driver.close()

    def __enter__(self):
        """Context manager entry point for automatic connection."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point for automatic connection closure."""
        self.close()

    def create_labeled_triple(self, subject: str, relation: str, object_: str, file_name: str):
        """
        Create a triple with a file-based label in the Neo4j graph.

        Args:
            subject (str): The subject of the triple.
            relation (str): The relationship between subject and object.
            object_ (str): The object of the triple.
            file_name (str): The base label for nodes.
        """
        label = f"Label_{file_name}"
        cleaned_relation = self._clean_relation(relation)

        # print("LABELL ",label)
        with self.driver.session() as session:
            session.write_transaction(
                self._create_and_link_with_label, 
                subject, cleaned_relation, object_, label
            )

    def create_unlabeled_triple(self, subject: str, relation: str, object_: str):
        """
        Create a triple with generic Entity labels in the Neo4j graph.

        Args:
            subject (str): The subject of the triple.
            relation (str): The relationship between subject and object.
            object_ (str): The object of the triple.
        """
        cleaned_relation = self._clean_relation(relation)
        with self.driver.session() as session:
            session.write_transaction(
                self._create_and_link_without_label, 
                subject, cleaned_relation, object_
            )

    
    def _clean_relation(self,relation: str) -> str:
        """
        Clean and format the relation string for Neo4j compatibility.

        Args:
            relation (str): The original relation string.

        Returns:
            str: Cleaned and formatted relation string.
        """
        return re.sub(r'[^a-zA-Z\s]', '', relation).replace(' ', '_')

    
    def _create_and_link_with_label(self,tx, subject, relation, object_param, label):
        """
        Neo4j transaction for creating triples with a specific label.

        Args:
            tx: Neo4j transaction.
            subject (str): The subject of the triple.
            relation (str): The cleaned relation.
            object_param (str): The object of the triple.
            label (str): The label for nodes.
        """
        query = (
            f"MERGE (a:{label} {{name: $subject}}) "
            f"MERGE (b:{label} {{name: $object_param}}) "
            f"MERGE (a)-[r:{relation}]->(b)"
        )
        tx.run(query, subject=subject, object_param=object_param)

    def _create_and_link_without_label(self, tx, subject, relation, object_param):
        query = (
            "MERGE (a:Entity {name: $subject}) "
            "MERGE (b:Entity {name: $object_param}) "
            f"MERGE (a)-[r:{relation}]->(b)"
        )
        # print(f"Parameters: subject={subject}, object={object_param}, relation={relation}")
        
        try:
            result = tx.run(query, subject=subject, object_param=object_param)
            # print("Transaction executed successfully")
        except Exception as e:
            print(f"Error in transaction: {e}")
            raise

    def read_triples_from_file(self,file_path: str):
        """
        Read triples from a text file.

        Args:
            file_path (str): Path to the file containing triples.

        Returns:
            List[Tuple[str, str, str]]: List of (subject, relation, object) triples.
        """
        triples = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.split(',')
                    if len(parts) >= 3:
                        subject, relation, object_ = parts[0], parts[1], parts[2]
                        triples.append((subject, relation, object_))
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
        return triples

    def process_single_file(self, file_path: str):
        """
        Process a single file and create triples in the Neo4j graph.

        Args:
            file_path (str): Path to the file to process.
        """
        triples = self.read_triples_from_file(file_path)
        for subject, relation, object_ in triples:
            self.create_unlabeled_triple(subject, relation, object_)

    def process_files_in_folder(self, folder_path: str, use_labels: bool = True):
        """
        Process all text files in a folder and create triples in the Neo4j graph.

        Args:
            folder_path (str): Path to the folder containing files.
            use_labels (bool, optional): Whether to use file-based labels. Defaults to False.
        """
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                file_name = filename.split('.')[0]

                triples = self.read_triples_from_file(file_path)
                for subject, relation, object_ in triples:
                    if use_labels:
                        self.create_labeled_triple(subject, relation, object_, file_name)
                    else:
                        self.create_unlabeled_triple(subject, relation, object_)

# def main():
#     """
#     Example usage of the Neo4j Knowledge Graph Handler.
#     """
#     # Example configuration
#     config_path = "/path/to/your/kg_config.yaml"

#     with Neo4jKnowledgeGraphHandler(config_path) as kg_handler:
#         # Option 1: Process a single file without labels
#         kg_handler.process_single_file("/path/to/your/input_file.txt")

#         # Option 2: Process all files in a folder with or without labels
#         kg_handler.process_files_in_folder("/path/to/your/input_folder", use_labels=False)

# if __name__ == "__main__":
#     main()
import os
import bs4
import validators
from urllib.parse import urlparse
from langchain.docstore.document import Document
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from itertools import chain
from docling.document_converter import DocumentConverter
import re
import requests
from bs4 import BeautifulSoup


class DataParser():
    def __init__(self):
        self.data_source = ""
        self.parsed_data = []
    
    def get_webpage_string(self,url):
        """
        Fetch webpage content and return as a clean string.
        
        Args:
            url (str): Website URL to fetch
        
        Returns:
            str: Extracted text content
        """
        try:
            # Fetch webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=100)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up excessive whitespace
            import re
            text = re.sub(r'\s+', ' ', text)
            
            return text
        
        except requests.RequestException as e:
            return f"Error fetching URL: {e}"

    def _check_path_type(self, path):
        """
        Determine the type of the input path.
        
        Args:
            path (str): Path to be checked
        
        Returns:
            str: Type of path (URL, File Path, Directory Path, or Unknown)
        """
        # Check if it's a URL
        if validators.url(path):
            return "URL"
        
        # Parse the path to check if it's a local file URL
        parsed_url = urlparse(path)
        if os.path.isfile(path):
            # Additional check for file extension
            _, ext = os.path.splitext(path)
            if ext.lower() in ['.txt', '.pdf']:
                return "File Path"
        
        # Check if it's a directory
        elif os.path.isdir(path):
            return "Directory Path"
        
        return "Unknown"

    def _txt_parser(self, path):
        """
        Parse a text file.
        
        Args:
            path (str): Path to the text file
        
        Returns:
            tuple: Containing file content and filename
        """
        with open(path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        return (file_content, os.path.basename(path))
    
    def _pdf_parser(self, path):
        """
        Parse a PDF file.
        
        Args:
            path (str): Path to the PDF file
        
        Returns:
            tuple: Containing PDF content and filename
        """
        try:
            # loader = PyPDFLoader(path)
            # pdf_pages = loader.load()
            
            # Combine all pages into a single text content
            # full_text = " ".join([page.page_content for page in pdf_pages])
            # PDF path or URL
            converter = DocumentConverter()
            result = converter.convert(path)
            return result.document.export_to_markdown(), os.path.basename(path)
        except Exception as e:
            print(f"Error parsing PDF {path}: {e}")
            return ("", os.path.basename(path))
    
    def _dir_parser(self, path):
        """
        Recursively parse files in a directory.
        
        Args:
            path (str): Path to the directory
        """
        for filename in os.listdir(path):
            full_path = os.path.join(path, filename)
            
            if os.path.isdir(full_path):
                self._dir_parser(full_path)
            elif filename.endswith('.txt'):
                file_content = self._txt_parser(full_path)
                x, y = file_content[0], file_content[1]
                self.parsed_data.append(Document(page_content=x, metadata={"filename": y}))
            elif filename.endswith('.pdf'):
                file_content = self._pdf_parser(full_path)
                x, y = file_content[0], file_content[1]
                self.parsed_data.append(Document(page_content=x, metadata={"filename": y}))
        return 

    def perform_parsing(self, data_source):
        """
        Main method to parse different types of data sources.

        Args:
            data_source (str): Path or URL to be parsed

        Returns:
            tuple: Parsed content as a single string and a unique identifier
        """
        # Reset parsed data
        self.parsed_data = []

        self.data_source = data_source
        path = self.data_source
        source_type = self._check_path_type(path)
        unique_identifier = None
        extracted_content = ""

        if source_type == "URL":
            try:
                final_url = "https://r.jina.ai/"+self.data_source
                extracted_content = self.get_webpage_string(final_url)

                clean_url = re.sub(r'^https?://', '', self.data_source)
    
                # Remove www. if present
                clean_url = re.sub(r'^www\.', '', clean_url)
                
                # Replace non-alphanumeric characters with underscores
                clean_url = re.sub(r'[^a-zA-Z0-9]+', '_', clean_url)
                unique_identifier = clean_url

            except Exception as e:
                print(f"Unexpected error parsing URL {self.data_source}: {e}")
            

            self.parsed_data.append(Document(page_content=extracted_content, metadata={"filename": self.data_source}))

        elif source_type == "File Path":
            _, ext = os.path.splitext(path)
            
            if ext.lower() == '.txt':
                File_output = self._txt_parser(self.data_source)
                file_content, file_name = File_output[0], File_output[1]
                self.parsed_data.append(Document(page_content=file_content, metadata={"filename": file_name}))
            
            elif ext.lower() == '.pdf':
                File_output = self._pdf_parser(self.data_source)
                file_content, file_name = File_output[0], File_output[1]
                self.parsed_data.append(Document(page_content=file_content, metadata={"filename": file_name}))
            
            unique_identifier = file_name
        
        elif source_type == "Directory Path":
            for filename in os.listdir(path):
                full_path = os.path.join(path, filename)
                
                if filename.endswith('.txt'):
                    file_content = self._txt_parser(full_path)
                    x, y = file_content[0], file_content[1]
                    self.parsed_data.append(Document(page_content=x, metadata={"filename": y}))
                
                elif filename.endswith('.pdf'):
                    file_content = self._pdf_parser(full_path)
                    x, y = file_content[0], file_content[1]
                    self.parsed_data.append(Document(page_content=x, metadata={"filename": y}))
                
                elif os.path.isdir(full_path):
                    self._dir_parser(full_path)
            
            unique_identifier = "unique_directory"

        # print(type(self.parsed_data))
        # print(self.parsed_data, unique_identifier)
        return self.parsed_data, unique_identifier

# Example usage (commented out)
# if __name__ == '__main__':
#     dp = DataParser()
#     parsed_docs, identifier = dp.perform_parsing("/path/to/your/file_or_directory")
#     for doc in parsed_docs:
#         print(f"Filename: {doc.metadata['filename']}")
#         print(f"Content: {doc.page_content[:200]}...")  # Print first 200 characters
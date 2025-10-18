from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageEmbeddings
from langchain_community.vectorstores import FAISS
import os

class DocumentProcessor:
    def __init__(self, persist_directory="./vectorstore"):
        self.chunk_size = 1000
        self.chunk_overlap = 100
        self.embedding_model = UpstageEmbeddings(
            api_key="",
            model="embedding-query"
        )
        self.persist_directory = persist_directory
        self.vectorstore = None
        
        # Load existing vectorstore if it exists
        self.load_vectorstore()

    def load_vectorstore(self):
        """Load vectorstore from disk if it exists"""
        if os.path.exists(self.persist_directory):
            try:
                self.vectorstore = FAISS.load_local(
                    self.persist_directory, 
                    self.embedding_model,
                    allow_dangerous_deserialization=True  # Be cautious with this
                )
                print(f"Loaded existing vectorstore from {self.persist_directory}")
            except Exception as e:
                print(f"Could not load vectorstore: {e}")
                self.vectorstore = None
        else:
            print("No existing vectorstore found. Will create new one.")

    def save_vectorstore(self):
        """Save vectorstore to disk"""
        if self.vectorstore is not None:
            self.vectorstore.save_local(self.persist_directory)
            print(f"Vectorstore saved to {self.persist_directory}")

    def load_document(self, file_path):
        """Load a document based on its file type"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        #elif file_path.endswith('.csv'):
            #loader = CSVLoader(file_path)
        elif file_path.endswith('.csv'):
            import pandas as pd
            from langchain.schema import Document
            
            # Read CSV
            df = pd.read_csv(file_path)
            df = df[pd.to_numeric(df['overall_score'], errors='coerce') > 8]
            df = df[df['original_user_prompt'] != df['prompt']]
            
            if 'prompt' in df.columns:
                prompts = df['prompt'].dropna()
            else:
                prompts = df.iloc[:, 2].dropna()
            
            docs = [Document(page_content=str(prompt)) for prompt in prompts]
            return docs        
            
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
        
        return loader.load()
    
    def process_document(self, file_path):
        """Process a document and add it to the vector store"""
        # Load the document
        docs = self.load_document(file_path)
        
        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap
        )
        split_docs = text_splitter.split_documents(docs)
        
        # Create or update the vector store
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(split_docs, self.embedding_model)
        else:
            self.vectorstore.add_documents(split_docs)
        
        # Save to disk after adding documents
        self.save_vectorstore()
            
    def retrieve_relevant_context(self, query, k=1):
        """Retrieve relevant document chunks for a query"""
        if self.vectorstore is None:
            return []
            
        return self.vectorstore.similarity_search(query, k=k)

    def reset(self):
        """Reset the document processor and delete persisted data"""
        self.vectorstore = None
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
            print(f"Deleted vectorstore from {self.persist_directory}")
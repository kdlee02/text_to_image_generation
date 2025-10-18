from document_processor import DocumentProcessor
from chat_engine import ChatEngine


class RAGChatbot:
    def __init__(self, persist_directory="./vectorstore"):
        self.document_processor = DocumentProcessor(persist_directory=persist_directory)
        self.chat_engine = ChatEngine()
        
    def upload_document(self, file_path):
        """Upload and process a document"""
        try:
            self.document_processor.process_document(file_path)
            return f"Document successfully processed and saved."
        except ValueError as e:
            return f"Error: {str(e)}"
        
    def send_message(self, message):
        """Send a message to the chatbot and get a response"""
        relevant_docs = self.document_processor.retrieve_relevant_context(message)
        
        context = ""
        for doc in relevant_docs:
            text = doc.page_content
            start = text.find("prompt: ")
            if start != -1:  
                prompt_text = text[start + len("prompt: "):]
                end = prompt_text.find("\n")
                if end != -1:
                    prompt_text = prompt_text[:end]
                context += f'{prompt_text.strip()}\n\n'  
            else:
                context += f'{text.strip()}\n\n'
        
        return self.chat_engine.send_message_exactly(message, context)
        
    def reset_conversation(self):
        """Reset the conversation history"""
        self.chat_engine.reset_conversation()
        return "Conversation history has been reset."
        
    def reset_documents(self):
        """Reset the document processor (including saved vectorstore)"""
        self.document_processor.reset() 
        return "Document knowledge has been reset."
        
    def reset_all(self):
        """Reset both conversation and documents"""
        self.reset_conversation()
        self.reset_documents()
        return "Both conversation history and document knowledge have been reset."
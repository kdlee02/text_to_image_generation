from langchain_upstage import ChatUpstage
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class ChatEngine:
    def __init__(self):
        self.chat_model = ChatUpstage(api_key="up_Dk6s7ks9NNd7SOKtFAO5ltetPMge0", model="solar-pro2")
        self.system_message = (
            "Your job is simple. do not fix anything and just print out exactly what the user typed"
        )
        
        # Define the prompt template with explicit system and human messages
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_message),
            HumanMessagePromptTemplate.from_template(
                "Context:\n{context}\n\nQuestion: {question}"
            )
        ])
        
        # Optionally, keep conversation history for display/logging only
        self.conversation_history = []

    def send_message(self, user_message, context=""):
        """Send a message to the chat engine and get a response"""
        # Format the messages using the prompt template (includes system message)
        messages = self.prompt.format_messages(
            context=context,
            question=user_message
        )
        # Get the response from the model
        response = self.chat_model.invoke(messages)
        
        # Optionally, track the conversation for display/logging
        self.conversation_history.append(HumanMessage(content=user_message))
        self.conversation_history.append(AIMessage(content=response.content))
        return response.content
    
    def send_message_exactly(self, user_message, context=""):
        """Send a message to the chat engine and get a response"""
        
        self.conversation_history.append(HumanMessage(content=user_message))
        self.conversation_history.append(AIMessage(content=context))
        return context

    def reset_conversation(self):
        """Reset the conversation history (for display/logging only)"""
        self.conversation_history = []
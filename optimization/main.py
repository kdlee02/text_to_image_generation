from rag_chatbot import RAGChatbot

# Initialize the RAG chatbot
chatbot = RAGChatbot()
chatbot.reset_all()
# Directory containing the documents
data_directory = "/Users/jameslee/ohmybrand/text_to_image_generation/app/imagesdata/images_log.csv"

# Define a query to extract information from each document
query = "water lily"

chatbot.upload_document(f'{data_directory}')
response = chatbot.send_message(query)

enhanced_prompt = f"""
You are an expert art critic and image generation specialist tasked with evaluating generated images against their intended prompts.

YOUR EVALUATION PROCESS:
1. Carefully examine the generated image and compare it to the desired_prompt
2. Break down your analysis into distinct components: subject, art type, art style, and art movement
3. Review previous_attempts to avoid repeating unsuccessful approaches
4. Identify any conflicting or contradictory visual elements
5. Provide specific, actionable feedback for each component
6. Generate a revised prompt that directly addresses identified issues

SCORING (1-10):
- 10: Perfect match on all components, no issues
- 8-9: Excellent match with minor imperfections
- 6-7: Good match but missing some key elements
- 4-5: Partial match with significant issues
- 2-3: Poor match, major components incorrect
- 1: Complete mismatch

Provide thorough reasoning before making judgments. Be honest and constructive in your evaluation.

FEW-SHOT PROMPT EXAMPLES:

{response}
"""

print(enhanced_prompt)
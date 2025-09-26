import fal_client
import os
from models.image_manager import ImageManager
from models.prompt_manager import PromptManager
from dotenv import load_dotenv

load_dotenv()

class ImageGeneratorService:
    def __init__(self):
        self.image_manager = ImageManager()
        # Ensure FAL_KEY is set from environment
        if not os.getenv('FAL_KEY'):
            raise ValueError("FAL_KEY environment variable is required for Fal AI")
    
    def generate_image(self, user_input: str) -> str:
        prompt = PromptManager.format_prompt(user_input)
        try:
            # Use Fal AI's Imagen4 model
            response = fal_client.run(
                "fal-ai/imagen4/preview",
                arguments={
                    "prompt": prompt,
                    "num_images": 1,
                    "aspect_ratio": "1:1",  # Default to square, can be made configurable
                }
            )
            
            if response and "images" in response and len(response["images"]) > 0:
                image_data = response["images"][0]
                # The image_data should contain the URL and other metadata
                return self.image_manager.add_image(prompt, image_data)
            else:
                raise RuntimeError("No image generated in response")
                
        except Exception as e:
            raise RuntimeError(f"Error generating image with Fal AI Imagen4: {str(e)}")
    
    def get_all_images(self):
        return self.image_manager.get_images()
    
    def get_csv_log(self):
        return self.image_manager.get_csv_log()
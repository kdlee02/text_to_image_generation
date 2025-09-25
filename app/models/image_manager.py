import base64
import requests
from PIL import Image
from io import BytesIO

class ImageManager:
    def __init__(self):
        self.images = []
        
    def image_to_base64(self, image_data):
        """Convert image data to base64. Handles both Google and Fal AI formats."""
        try:
            # Handle Fal AI format (URL-based)
            if isinstance(image_data, dict) and "url" in image_data:
                response = requests.get(image_data["url"])
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                return base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # Handle Google format (legacy support)
            elif hasattr(image_data, 'image') and hasattr(image_data.image, 'image_bytes'):
                image_bytes = image_data.image.image_bytes
                image = Image.open(BytesIO(image_bytes))
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                return base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            else:
                raise ValueError("Unsupported image data format")
                
        except Exception as e:
            raise RuntimeError(f"Error processing image: {str(e)}")
        
    def add_image(self, prompt, image_data):
        image_base64 = self.image_to_base64(image_data)
        
        # Extract additional metadata from Fal AI response
        metadata = {}
        if isinstance(image_data, dict):
            metadata = {
                "url": image_data.get("url"),
                "width": image_data.get("width"),
                "height": image_data.get("height"),
                "content_type": image_data.get("content_type")
            }
        
        image_entry = {
            "id": len(self.images), 
            "prompt": prompt, 
            "image_base64": image_base64,
            "metadata": metadata
        }
        self.images.append(image_entry)
        return image_base64
    
    def get_images(self):
        return self.images
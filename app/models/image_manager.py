import base64
import requests
from PIL import Image
from io import BytesIO
import os
import csv
from datetime import datetime

class ImageManager:
    def __init__(self):
        self.images = []
        # Set up the imagesdata directory
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.images_dir = os.path.join(self.base_dir, "imagesdata")
        self.csv_file = os.path.join(self.images_dir, "images_log.csv")
        
        # Ensure the directory exists
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Initialize CSV file with headers if it doesn't exist
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'timestamp', 'image_id', 'original_user_prompt', 'prompt', 'image_url', 'local_filename', 'width', 'height',
                    'subject_match', 'art_type_match', 'art_style_match', 'art_movement_match', 
                    'overall_prompt_match', 'has_conflicting_elements',
                    'subject_feedback', 'art_type_feedback', 'art_style_feedback', 'art_movement_feedback',
                    'overall_feedback', 'conflict_description','overall_score'
                ])
        
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
            
            else:
                raise ValueError("Unsupported image data format")
                
        except Exception as e:
            raise RuntimeError(f"Error processing image: {str(e)}")
        
    def add_image(self, prompt, image_data, dspy_result=None, original_user_prompt=None):
        image_base64 = self.image_to_base64(image_data)
        
        # Extract additional metadata from Fal AI response
        metadata = {}
        image_url = ""
        width = height = None
        
        if isinstance(image_data, dict):
            metadata = {
                "url": image_data.get("url"),
                "width": image_data.get("width"),
                "height": image_data.get("height"),
                "content_type": image_data.get("content_type")
            }
            image_url = image_data.get("url", "")
            width = image_data.get("width")
            height = image_data.get("height")
        
        # Generate unique image ID and filename
        image_id = len(self.images)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}_{image_id}.jpg"
        filepath = os.path.join(self.images_dir, filename)
        
        # Save image to file
        try:
            # Download and save the image
            if image_url:
                response = requests.get(image_url)
                response.raise_for_status()
                with open(filepath, 'wb') as f:
                    f.write(response.content)
            else:
                # Fallback: save from base64
                image_bytes = base64.b64decode(image_base64)
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
        except Exception as e:
            print(f"Warning: Could not save image file: {str(e)}")
            filename = ""  # Clear filename if save failed
        
        # Extract DSPy evaluation data if provided
        subject_match = dspy_result.subject_match if dspy_result else None
        art_type_match = dspy_result.art_type_match if dspy_result else None
        art_style_match = dspy_result.art_style_match if dspy_result else None
        art_movement_match = dspy_result.art_movement_match if dspy_result else None
        overall_prompt_match = dspy_result.overall_prompt_match if dspy_result else None
        has_conflicting_elements = dspy_result.has_conflicting_elements if dspy_result else None
        
        subject_feedback = dspy_result.subject_feedback if dspy_result else None
        art_type_feedback = dspy_result.art_type_feedback if dspy_result else None
        art_style_feedback = dspy_result.art_style_feedback if dspy_result else None
        art_movement_feedback = dspy_result.art_movement_feedback if dspy_result else None
        overall_feedback = dspy_result.overall_prompt_match_feedback if dspy_result else None
        conflict_description = dspy_result.conflict_description if dspy_result else None
        overall_score = dspy_result.overall_score if dspy_result else None
        # Log to CSV
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().isoformat(),
                    image_id,
                    original_user_prompt,
                    prompt,
                    image_url,
                    filename,
                    width,
                    height,
                    subject_match,
                    art_type_match,
                    art_style_match,
                    art_movement_match,
                    overall_prompt_match,
                    has_conflicting_elements,
                    subject_feedback,
                    art_type_feedback,
                    art_style_feedback,
                    art_movement_feedback,
                    overall_feedback,
                    conflict_description,
                    overall_score
                ])
        except Exception as e:
            print(f"Warning: Could not write to CSV log: {str(e)}")
        
        image_entry = {
            "id": image_id, 
            "prompt": prompt, 
            "image_base64": image_base64,
            "metadata": metadata,
            "local_filename": filename
        }
        self.images.append(image_entry)
        return image_base64
    
    def get_images(self):
        return self.images
    
    def get_csv_log(self):
        """Read and return the CSV log data"""
        if not os.path.exists(self.csv_file):
            return []
        
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            print(f"Error reading CSV log: {str(e)}")
            return []
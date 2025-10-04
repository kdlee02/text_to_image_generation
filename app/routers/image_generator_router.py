from services.dspy_optimization import ImageGeneratorService
from models.image_manager import ImageManager

class ImageGeneratorRouter:
    def __init__(self):
        self.image_generator = ImageGeneratorService()
    
    def generate_image(self, user_input):
        if not user_input:
            return {'error': 'Missing input'}, 400
        try:
            base64_image = self.image_generator.dspy_opt(user_input)
            #base64_image = dspy_opt(user_input)
            
            return {'image': base64_image}
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get_images(self):
        images = self.image_generator.get_all_images()
        return {'images': images}
    
    def get_csv_log(self):
        csv_data = self.image_generator.get_csv_log()
        return {'csv_data': csv_data}
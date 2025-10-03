from services.image_generator_service import ImageGeneratorService
from models.image_manager import ImageManager
from services.dspy_optimization import dspy_opt

class ImageGeneratorRouter:
    def __init__(self):
        self.image_generator = ImageManager()
    
    def generate_image(self, user_input):
        if not user_input:
            return {'error': 'Missing input'}, 400
        try:
            #base64_image = self.image_generator_service.generate_image(user_input)
            base64_image = dspy_opt(user_input)
            
            return {'image': base64_image}
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get_images(self):
        images = self.image_generator.get_images()
        return {'images': images}
    
    def get_csv_log(self):
        csv_data = self.image_generator.get_csv_log()
        return {'csv_data': csv_data}
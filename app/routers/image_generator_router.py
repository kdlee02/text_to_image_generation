from services.image_generator_service import ImageGeneratorService

class ImageGeneratorRouter:
    def __init__(self):
        self.image_generator_service = ImageGeneratorService()
    
    def generate_image(self, user_input):
        if not user_input:
            return {'error': 'Missing input'}, 400
        try:
            base64_image = self.image_generator_service.generate_image(user_input)
            return {'image': base64_image}
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get_images(self):
        images = self.image_generator_service.get_all_images()
        return {'images': images}
    
    def get_csv_log(self):
        csv_data = self.image_generator_service.get_csv_log()
        return {'csv_data': csv_data}
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

class CrossModalIntegrator:
    def __init__(self):
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def image_to_recipe(self, image_path):
        image = Image.open(image_path)
        pixel_values = self.feature_extractor(images=image, return_tensors="pt").pixel_values
        output_ids = self.model.generate(pixel_values.to(self.device))
        recipe = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return recipe

    def text_to_image_search(self, text_query):
        # Implement semantic search against image database
        return ["food_images/salad.jpg", "food_images/soup.jpg"]
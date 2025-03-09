from transformers import BertTokenizer, BertModel
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class NutritionQueryProcessor:
    def __init__(self):
        try:
            # Use the Auto classes for better compatibility
            self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
            self.model = AutoModel.from_pretrained('bert-base-uncased')
        except Exception as e:
            print(f"Error loading model: {e}")
            self._download_fallback()
        self.allergy_labels = [
        'dairy', 'nuts', 'gluten', 'seafood', 'eggs', 
        'soy', 'vegetarian', 'vegan', 'kosher', 'halal'
        ]
    def _download_fallback(self):
        """Alternative download method"""
        from huggingface_hub import snapshot_download
        try:
            snapshot_download(repo_id="bert-base-uncased")
            self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
            self.model = AutoModel.from_pretrained('bert-base-uncased')
        except Exception as e:
            raise RuntimeError(f"Failed to download model: {e}")
        
    def detect_allergies(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        
        # Simple cosine similarity check (replace with trained classifier)
        allergy_embeddings = np.array([self._get_embedding(label) for label in self.allergy_labels])
        similarities = np.dot(embeddings, allergy_embeddings.T)
        return [self.allergy_labels[i] for i in np.where(similarities > 0.7)[1]]
    
    def _get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        return self.model(**inputs).last_hidden_state.mean(dim=1).detach().numpy()
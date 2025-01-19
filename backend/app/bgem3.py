from FlagEmbedding import BGEM3FlagModel
import torch

class BGEM3Service:
    def __init__(self, model_name="BAAI/bge-m3"):
        self.model = BGEM3FlagModel(model_name, use_fp16=True)

    def embed_text(self, text: str, max_length=1024):
        try:
            with torch.no_grad():
                # Generate the embedding using the model's encode method
                embedding = self.model.encode([text], max_length=max_length)['dense_vecs'][0]

                # Convert embedding to a NumPy array
                embedding = torch.tensor(embedding).numpy()

            return embedding.tolist()
        
        except Exception as e:
            print(f"Error embedding text: {e}")
            return None
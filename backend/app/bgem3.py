from FlagEmbedding import FlagModel

class BGEM3Service:
    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        self.model = FlagModel(model_name, use_fp16=True)

    def embed_text(self, text: str, max_length=512):
        try:
            # Generate the embedding using the model's encode method
            embedding = self.model.encode(text, max_length=max_length)

            # Convert embedding to a list for return
            return embedding.tolist()
        
        except Exception as e:
            print(f"Error embedding text: {e}")
            return None
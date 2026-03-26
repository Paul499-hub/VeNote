import torch
from sentence_transformers import SentenceTransformer

print("CUDA available:", torch.cuda.is_available())
print("GPU name:", torch.cuda.get_device_name(0))

model = SentenceTransformer("BAAI/bge-small-en", device="cuda")

emb = model.encode(["Hello GPU world!"], convert_to_tensor=True)
print("Embedding shape:", emb.shape)
print("Embedding first 5 values:", emb[0][:5])

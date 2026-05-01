from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
# Modules
from app.core.config import settings


# ----------- Embedding into vectors for qdrant models
embedding_model = SentenceTransformer(settings.embedding_model, trust_remote_code=True)

# ----------- AI for variant_vector generation
vv_model_name = "Qwen/Qwen2.5-3B-Instruct"
#vv_model_name = "Qwen/Qwen3-4B-Instruct-2507"
#vv_model_name = "Qwen/Qwen2.5-14B-Instruct"
vv_tokenizer = AutoTokenizer.from_pretrained(vv_model_name)
vv_model = AutoModelForCausalLM.from_pretrained(
    vv_model_name,
    dtype="auto",
    device_map="auto",
)
# Qwen/Qwen3-4B-Instruct-2507
# microsoft/Phi-4-mini-instruct
# google/gemma-3-4b-it
print(f"[vv_model device_map]:{vv_model.hf_device_map}")
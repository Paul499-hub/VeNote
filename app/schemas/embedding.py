from pydantic import BaseModel, Field

# Router input schemas
class IN_TextEmbedRequest(BaseModel):
    text: str

class IN_SimilaritySearchRequest(BaseModel):
    text: str
    args_limit: int = Field(gt=0, lt=999)

# Function output schemas
class F_EmbedTextOut(BaseModel):
    status: str
    vector: list[float]
    vector_size: int

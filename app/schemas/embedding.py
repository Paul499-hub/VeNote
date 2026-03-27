from pydantic import BaseModel

class TextEmbedRequest(BaseModel):
    text: str
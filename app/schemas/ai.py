from pydantic import BaseModel, Field

class AiInput(BaseModel):
    msg: str = Field(min_lenth=1, max_length=999)
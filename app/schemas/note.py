from pydantic import BaseModel, Field, ConfigDict

class NoteCreate(BaseModel):
    text: str
    title: str | None = None

class Note(BaseModel):
    id: int = Field(gt=0, lt=99999)
    text: str
    
    model_config = ConfigDict(from_attributes=True)
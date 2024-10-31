from pydantic import BaseModel, Field
from typing import Optional

class XVariableModel(BaseModel):
    xvid:Optional[str]=""
    description:Optional[str]=""
    type: str
    value: str
    parent_id: Optional[str] = None  # References the _id of a related record in the observatory or another variable
from pydantic import BaseModel, Field
from typing import Optional
from ocaapi.models import PyObjectId
class ObservatoryModel(BaseModel):
    obid: str
    title: str
    description: Optional[str]
    image: Optional[str] = "https://static.vecteezy.com/system/resources/thumbnails/004/141/669/small/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg"
    disabled: Optional[bool]= False

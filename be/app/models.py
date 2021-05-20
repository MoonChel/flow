from typing import List, Optional

from pydantic import BaseModel


class FormField(BaseModel):
    name: str


class Form(BaseModel):
    fields: List[FormField]


class Step(BaseModel):
    name: str
    form: Optional[Form]


class Process(BaseModel):
    name: str
    steps: List[Step]

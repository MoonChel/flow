from typing import Dict, List, Optional

from pydantic import BaseModel


class FormField(BaseModel):
    name: str
    label: str
    type: str
    validation: List[str]


class Form(BaseModel):
    fields: List[FormField]


class Step(BaseModel):
    name: str
    active: bool
    form: Optional[Form]
    form_value: Optional[Dict]


class Process(BaseModel):
    name: str
    steps: List[Step]

    def get_active_step(self) -> Optional[Step]:
        step = None

        for s in self.steps:
            if s.active:
                step = s

        return step

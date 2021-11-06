from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field


class FormField(BaseModel):
    name: str
    label: str
    type: str
    validation: List[str]


class FormAction(BaseModel):
    name: str
    label: str


class Form(BaseModel):
    fields: List[FormField] = Field(default_factory=list)
    actions: List[FormAction] = Field(default_factory=list)


class Condition(BaseModel):
    name: str
    label: str
    values: Dict[Union[str, int, bool], str]

    def evaluate(self, action: str) -> str:
        return self.values.get(action)


class StepAction(BaseModel):
    name: str
    label: str


class Step(BaseModel):
    name: str
    label: str
    form: Optional[Form]
    condition: Optional[Condition]
    active: bool = Field(False)
    form_value: Optional[Dict[str, Any]]
    actions: List[StepAction] = Field(default_factory=list)
    next_step_name: Optional[str]


class Process(BaseModel):
    name: str
    label: str
    steps: List[Step]

    def get_active_step(self) -> Optional[Step]:
        step = None

        for s in self.steps:
            if s.active:
                step = s

        return step

    def go_to_next_step(self) -> Optional[Step]:
        step = self.get_active_step()

        if not step:
            return None

        next_step = self.get_step_by_name(step.next_step_name)

        if not step:
            return None

        step.active = False
        next_step.active = True

        return next_step

    def get_step_by_name(self, name: str) -> Optional[Step]:
        step = None

        for s in self.steps:
            if name == s.name:
                step = s

        return step

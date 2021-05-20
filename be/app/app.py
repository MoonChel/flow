from fastapi import FastAPI, HTTPException

app = FastAPI()

from .models import Process, Step, Form, FormField

recruitment = Process(
    name="recruiting",
    steps=[
        Step(
            name="fill_form",
            form=Form(
                fields=[
                    FormField(name="name"),
                    FormField(name="surname"),
                ]
            ),
            active=True,
        ),
        Step(
            name="finish",
            active=False,
        ),
    ],
)


@app.get("/process")
async def get_process():
    return recruitment.dict()


@app.get("/process-step")
async def get_next_step():
    step = recruitment.get_active_step()

    if not step:
        raise HTTPException(404, "Active step not found")

    return step.dict()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

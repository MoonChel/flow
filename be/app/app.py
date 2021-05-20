from fastapi import FastAPI, Request, HTTPException

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .models import Process, Step, Form, FormField

recruitment = Process(
    name="recruiting",
    steps=[
        Step(
            name="fill_form",
            form=Form(
                fields=[
                    FormField(
                        name="name",
                        label="Name",
                        type="text",
                        validation=["required"],
                    ),
                    FormField(
                        name="lastname",
                        label="Lastname",
                        type="text",
                        validation=["required"],
                    ),
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


@app.post("/process-step")
async def save_step_result(request: Request):
    step = recruitment.get_active_step()

    if not step:
        raise HTTPException(404, "Active step not found")

    step.form_value = await request.json()

    return step.dict()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

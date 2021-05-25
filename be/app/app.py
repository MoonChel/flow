import enum
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

from .models import Process, Step, Form, FormField, FormAction, Condition, StepAction


class RECRUITMENT_STEP(enum.Enum):
    FILL_APPLICATION_FORM = "FILL_APPLICATION_FORM"
    REVIEW_APPLICATION_FORM = "REVIEW_APPLICATION_FORM"
    CONDITION_REVIEW_FORM = "CONDITION_REVIEW_FORM"
    REVIEW_PHONE_INTERVIEW = "PHONE_INTERVIEW"
    CONDITION_REVIEW_PHONE_INTEVIEW = "CONDITION_REVIEW_PHONE_INTEVIEW"
    REVIEW_FACE_TO_FACE_INTERVIEW = "REVIEW_FACE_TO_FACE_INTERVIEW"
    CONDITION_REVIEW_FACE_TO_FACE_INTERVIEW = "CONDITION_REVIEW_FACE_TO_FACE_INTERVIEW"
    APPROVE_APPLICANT = "APPROVE_APPLICANT"
    REJECT_APPLICANT = "REJECT_APPLICANT"
    FINISH = "FINISH"


recruitment = Process(
    name="recruitment_form",
    label="Recruitment Process",
    steps=[
        Step(
            name=RECRUITMENT_STEP.FILL_APPLICATION_FORM.value,
            label="New application form",
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
                ],
                actions=[
                    FormAction(name="submit", label="Submit"),
                ],
            ),
            active=True,
            next_step_name=RECRUITMENT_STEP.REVIEW_APPLICATION_FORM.value,
        ),
        Step(
            name=RECRUITMENT_STEP.REVIEW_APPLICATION_FORM.value,
            label="Review application form",
            form=Form(
                name="review_application_form",
                label="Review application form",
                actions=[
                    FormAction(name="yes", label="Passed"),
                    FormAction(name="no", label="Didn't pass"),
                ],
            ),
            next_step_name=RECRUITMENT_STEP.CONDITION_REVIEW_FORM.value,
        ),
        Step(
            name=RECRUITMENT_STEP.CONDITION_REVIEW_FORM.value,
            label="Passed review for application form?",
            condition=Condition(
                name="condition_1",
                label="Phone interview or Rejection email",
                values={
                    "yes": RECRUITMENT_STEP.REVIEW_PHONE_INTERVIEW.value,
                    "no": RECRUITMENT_STEP.REJECT_APPLICANT.value,
                },
            ),
        ),
        Step(
            name=RECRUITMENT_STEP.REVIEW_PHONE_INTERVIEW.value,
            label="Review phone interview",
            form=Form(
                name="review_phone_inteview",
                label="Review phone inteview",
                fields=[
                    FormField(
                        name="comment",
                        label="Comment",
                        type="text",
                        validation=["required"],
                    ),
                ],
                actions=[
                    FormAction(name="yes", label="Passed"),
                    FormAction(name="no", label="Did not pass"),
                ],
            ),
            next_step_name=RECRUITMENT_STEP.CONDITION_REVIEW_PHONE_INTEVIEW.value,
        ),
        Step(
            name=RECRUITMENT_STEP.CONDITION_REVIEW_PHONE_INTEVIEW.value,
            label="Passed phone interview?",
            condition=Condition(
                name="condition_1",
                label="Face to face interview or Rejection email",
                values={
                    "yes": RECRUITMENT_STEP.REVIEW_FACE_TO_FACE_INTERVIEW.value,
                    "no": RECRUITMENT_STEP.REJECT_APPLICANT.value,
                },
            ),
        ),
        Step(
            name=RECRUITMENT_STEP.REVIEW_FACE_TO_FACE_INTERVIEW.value,
            label="Review face to face inteview",
            form=Form(
                name="review_face_to_face_interview",
                label="Review face to face interview form",
                fields=[
                    FormField(
                        name="comment",
                        label="Comment",
                        type="text",
                        validation=["required"],
                    ),
                ],
                actions=[
                    FormAction(name="yes", label="Passed"),
                    FormAction(name="no", label="Did not pass"),
                ],
            ),
            next_step_name=RECRUITMENT_STEP.CONDITION_REVIEW_FACE_TO_FACE_INTERVIEW.value,
        ),
        Step(
            name=RECRUITMENT_STEP.CONDITION_REVIEW_FACE_TO_FACE_INTERVIEW.value,
            label="Passed face to face interview?",
            condition=Condition(
                name="condition_1",
                label="Send approved or Rejection email",
                values={
                    "yes": RECRUITMENT_STEP.APPROVE_APPLICANT.value,
                    "no": RECRUITMENT_STEP.REJECT_APPLICANT.value,
                },
            ),
        ),
        Step(
            name=RECRUITMENT_STEP.APPROVE_APPLICANT.value,
            label="Approve applicant",
            actions=[
                StepAction(
                    name="send_approved_email",
                    label="Send approved email",
                ),
            ],
            next_step_name=RECRUITMENT_STEP.FINISH.value,
        ),
        Step(
            name=RECRUITMENT_STEP.REJECT_APPLICANT.value,
            label="Reject applicant",
            actions=[
                StepAction(
                    name="send_rejection_email",
                    label="Send rejection email",
                ),
            ],
            next_step_name=RECRUITMENT_STEP.FINISH.value,
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
        raise HTTPException(404, "Active step is not found")

    return step.dict()


@app.post("/process-step")
async def save_step_result(request: Request):
    step = recruitment.get_active_step()

    if not step:
        raise HTTPException(404, "Active step is not found")

    step.form_value = await request.json()

    # moving to next step
    next_step = recruitment.go_to_next_step()

    if not next_step:
        raise HTTPException(404, "Next step is not found")

    if next_step.condition:
        next_next_step_name = next_step.condition.evaluate(step.form_value["action"])

        if not next_next_step_name:
            raise HTTPException(404, f"Next step is not found: {next_next_step_name}")

        next_next_step = recruitment.get_step_by_name(next_next_step_name)

        if not next_next_step:
            raise HTTPException(404, f"Next step is not found: {next_next_step_name}")

        step.active = False
        next_next_step.active = True

    return step.dict()

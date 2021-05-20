from app.models import Process, Step, Form, FormField


def test_process():
    p = Process(
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
            ),
            Step(name="finish"),
        ],
    )

    print(p.json())

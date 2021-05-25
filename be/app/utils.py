from graphviz import Digraph
from .models import Process


def gen_graph(process: Process) -> str:
    dot = Digraph(comment=process.name)

    for step in process.steps:
        shape = "ellipse"

        if step.condition:
            shape = "diamond"
        elif step.actions:
            shape = "polygon"

        dot.node(step.name, step.label, shape=shape)

    for step in process.steps:
        if step.condition:
            for action, next_step_name in step.condition.values.items():
                next_step = process.get_step_by_name(next_step_name)

                dot.edge(step.name, next_step.name, label=action)
        else:
            dot.edge(step.name, step.next_step_name)

    return dot.render(process.name + ".gv", format="png")

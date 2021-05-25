from graphviz import Digraph

from app.app import recruitment


def gen_graph():
    dot = Digraph(comment=recruitment.name)

    for step in recruitment.steps:
        shape = "ellipse"

        if step.condition:
            shape = "diamond"
        elif step.actions:
            shape = "polygon"

        dot.node(step.name, step.label, shape=shape)

    for step in recruitment.steps:
        if step.condition:
            for action, next_step_name in step.condition.values.items():
                next_step = recruitment.get_step_by_name(next_step_name)

                dot.edge(step.name, next_step.name, label=action)
        else:
            dot.edge(step.name, step.next_step_name)

    dot.render(recruitment.name + ".gv", format="png")


if __name__ == "__main__":
    gen_graph()

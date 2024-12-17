import reflex as rx

from ..style import tooltip_styles, info
from ...wrappers.state import ComponentWrapperState

from typing import Any

def linechart_v1(
    data: rx.Var[list[dict[str, Any]]],
    x: rx.Var[str],
    y: rx.Var[str] | rx.Var[list[str]] | None = None,
    x_label: rx.Var[str] | None = None,
    # y_label: rx.Var[str] | None = None,
    # color: rx.Var[str] | None = None,
    # horizontal: rx.Var[bool] = False,
    # height: rx.Var[int] = rx.Var.create(250),
):
    """Graph data in a line chart.

    Example usage:
    class State(rx.State):
        # INCLUDE FULL TYPE ANNOTATION!
        data: list[dict[str, Any]] = [
            {"name": "John", "age": 30, "city": "New York"},
        ]
    ...

    # Always prefer to hook up to state!
    linechart_v1(data=State.data, x="name", y=["age"], x_label="Name")
    """

    return rx.center(
        rx.vstack(
            rx.recharts.line_chart(
                rx.recharts.graphing_tooltip(
                    **vars(tooltip_styles),
                    custom_attrs={"display": "flex", "justify-content": "space-between"}
                ),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    fill_opacity=0.5,
                    stroke=rx.color("slate", 5),
                ),
                rx.foreach(
                    y,
                    lambda name, index: rx.recharts.line(
                        data_key=name,
                        stroke=ComponentWrapperState.default_theme[index],
                        type_="natural",
                        dot=False,
                    ),
                ),
                rx.recharts.x_axis(
                    data_key=x,
                    label=x_label,
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    custom_attrs={"fontSize": "12px"},
                ),
                data=data,
                width="100%",
                height=250,
                margin={"left": 20},
            ),
            width="100%",
            margin_right="20px",
        ),
        width="100%",
        padding="0.5em",
    )

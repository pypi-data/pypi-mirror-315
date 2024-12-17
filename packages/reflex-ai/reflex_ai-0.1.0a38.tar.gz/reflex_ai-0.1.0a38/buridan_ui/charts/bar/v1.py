import reflex as rx

from ..style import tooltip_styles, info
from ...wrappers.state import ComponentWrapperState

from typing import Any

def barchart_v1(
    data: rx.Var[list[dict[str, Any]]],
    x: rx.Var[str],
    y: rx.Var[str] | rx.Var[list[str]] | None = None,
    x_label: rx.Var[str] | None = None,
    # y_label: rx.Var[str] | None = None,
    # color: rx.Var[str] | None = None,
    # horizontal: rx.Var[bool] = False,
    # height: rx.Var[int] = rx.Var.create(250),
):
    """Graph data in a bar chart.

    Example usage:
    class State(rx.State):
        # INCLUDE FULL TYPE ANNOTATION!
        data: list[dict[str, Any]] = [
            {"name": "John", "age": 30, "city": "New York"},
        ]
    ...

    # Always prefer to hook up to state!
    barchart_v1(data=State.data, x="name", y=["age"], x_label="Name")
    """

    return rx.center(
        rx.vstack(
            rx.recharts.bar_chart(
                rx.recharts.graphing_tooltip(**vars(tooltip_styles)),
                rx.recharts.cartesian_grid(horizontal=True, vertical=False),
                rx.foreach(
                    y,
                    lambda name, index: rx.recharts.bar(
                        data_key=name,
                        fill=ComponentWrapperState.default_theme[index],
                        radius=6,
                    ),
                ),
                rx.recharts.x_axis(
                    data_key=x,
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    label=x_label,
                ),
                data=data,
                width="100%",
                height=250,
                bar_size=50,
                bar_gap=2,
                bar_category_gap="0%",
            ),
            width="100%",
        ),
        width="100%",
        padding="0.5em",
    )

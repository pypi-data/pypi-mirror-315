import reflex as rx

from ..style import tooltip_styles, info
from ...wrappers.state import ComponentWrapperState

from typing import Any


def areachart_v1(
    data: rx.Var[list[dict[str, Any]]],
    x: rx.Var[str],
    y: rx.Var[str] | rx.Var[list[str]] | None = None,
    x_label: rx.Var[str] | None = None,
    # color: rx.Var[str] | None = None,
    # horizontal: rx.Var[bool] = False,
    # width: rx.Var[str] | None = None,
    # height: rx.Var[int] | None = None,
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
            rx.recharts.area_chart(
                rx.recharts.graphing_tooltip(**vars(tooltip_styles)),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    fill_opacity=0.5,
                    stroke=rx.color("slate", 5),
                ),
                rx.foreach(
                    y,
                    lambda name, index: rx.recharts.area(
                        data_key=name,
                        fill=ComponentWrapperState.default_theme[index],
                        stroke=ComponentWrapperState.default_theme[index],
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
                margin={"left": 20},
            ),
            width="100%",
            margin_right="20px",
        ),
        width="100%",
        padding="0.5em",
    )

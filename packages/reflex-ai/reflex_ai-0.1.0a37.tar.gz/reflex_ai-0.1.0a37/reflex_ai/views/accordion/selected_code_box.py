import reflex as rx
from reflex_ai.components.hint import hint
from reflex_ai.components.code_block import code_block
from reflex_ai.selection import ClickSelectionState


def selected_code_pill(text: str) -> rx.Component:
    return hint(
        text="Open in IDE",
        content=rx.link(
            rx.el.button(
                text,
                class_name="max-w-fit border-[--slate-5] bg-[--slate-3] px-3 py-[0.275rem] border rounded-[62.5rem] font-small text-[--slate-11] cursor-pointer",
            ),
            href=ClickSelectionState.selected_code_ide_hyperlink,
            is_external=True,
            class_name="w-fit",
        ),
        side="right",
    )


def selected_code_box() -> rx.Component:
    return rx.box(
        # Show the selected filename
        rx.cond(
            ClickSelectionState.selected_code_filename_and_line_range,
            selected_code_pill(
                ClickSelectionState.selected_code_filename_and_line_range
            ),
            rx.fragment(),
        ),
        # Show the selected code
        code_block(
            rx.cond(
                ClickSelectionState.code,
                ClickSelectionState.code,
                "Select a component to edit",
            )
        ),
        class_name="flex flex-col gap-3 w-full",
    )

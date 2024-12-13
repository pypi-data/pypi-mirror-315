"""The local AI toolbar to hook up with the server-side reflex agent."""

import reflex as rx
from reflex.utils import console
from reflex_ai.selection import ClickSelectionState
from reflex_ai.local_agent import (
    LocalAgent,
    InternResponse,
    InternRequest,
    Diff,
    TOOLS_HR_NAMES,
)
from reflex_ai.utils import path_utils


class ToolbarState(rx.State):
    """The toolbar state."""

    tools_used: list[str] = ["Preparing request"]
    current_step: str = "selected_code"  # The current step name of the process (selected_code, processing, review_changes)
    processing: bool = False
    selected_id: str = ""
    code: str = ""
    prompt: str = ""
    step: int = 0
    diff: list[Diff] = []
    selected_diff: Diff = Diff(filename="", diff="")  # The selected diff
    changes_comment: str = ""
    thread_id: str = ""
    _agent: LocalAgent = LocalAgent()

    @rx.background
    async def process(self, prompt: dict[str, str]):
        """Process the user's prompt.

        Args:
            prompt: The prompt from the user from the form input.

        Yields:
            Updates to the frontend.
        """
        # Set the processing flag to True.
        async with self:
            self.thread_id = ""
            self.start_processing()
            self.prompt = prompt["prompt"]
            selection_state = await self.get_state(ClickSelectionState)
        yield

        # Create the intern request.
        request = InternRequest(
            prompt=prompt["prompt"],
            selected_code=selection_state.code,
            selected_module=selection_state.selection.get_selection_module(),
            selected_function=selection_state.selection.function_name,
            parent_component=selection_state.selection.modules[-1],
        )

        # Process the messages with the local agent.
        async for response in self._agent.process(request):
            console.info(response)
            async with self:
                # Check if it's an InternResponse.
                if isinstance(response, InternResponse):
                    self.thread_id = response.thread_id
                    if response.final_message:
                        # TODO: set the final message in the state.
                        break

                # It's a tool use message.
                else:
                    self.tools_used.append(
                        TOOLS_HR_NAMES.get(response.name, response.name)
                    )
            yield

        async with self:
            self.finish_processing()
        yield
        # Trigger a hot reload.
        self.trigger_reload()

    def start_processing(self):
        self.tools_used = [self.tools_used[0]]
        self.processing = True
        self.current_step = "processing"
        self.step = 1

    def finish_processing(self):
        self.selected_diff = self.diff[0]
        # self.changes_comment = json.dumps(self.messages[-1].content)
        self.current_step = "review_changes"
        self.step = 2
        self.processing = False

    async def confirm_change(self, accepted: bool):
        """Accept the current diff.

        Args:
            accepted: Whether the diff is accepted or not.
        """
        thread_id, diff = self.thread_id, self.diff
        self.reset()
        await self._agent.confirm_change(thread_id, diff, accepted)
        if not accepted:
            self.trigger_reload()

    def trigger_reload(self):
        """Trigger a hot reload."""
        config = rx.config.get_config()
        app_name = config.app_name
        filename = f"{app_name}/{app_name}.py"
        contents = open(filename).read()
        with open(filename, "w") as f:
            f.write(contents)

    def load_diff(self):
        diff = path_utils.directory_diff()
        self.diff = [
            Diff(filename=str(filename), diff="\n".join(diff))
            for filename, diff in diff.items()
            if (len(diff) > 0 or ("__init__.py" in filename))
        ]

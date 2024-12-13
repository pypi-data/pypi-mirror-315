"""The agent that runs on the user's local client."""

import dataclasses
import difflib
import importlib
import json
import os

import httpx
from flexai import Agent
from flexai.message import ToolCall, ToolResult
from pydantic import BaseModel
from reflex.utils import console

import reflex as rx
from reflex_ai.utils import ast_utils, codegen, path_utils
from reflex_ai import paths
from reflex_cli.v2.utils import hosting


# NOTE: using BaseModel here instead of rx.Base due to FastAPI not liking the v1 models
class InternRequest(BaseModel):
    """The request to the AI intern."""

    prompt: str
    selected_code: str
    selected_module: str
    selected_function: str
    parent_component: dict[str, str]


class InternResponse(BaseModel):
    """The response from the AI intern."""

    thread_id: str
    tool_calls: list[ToolCall] = []
    final_message: str = ""


class ToolRequestResponse(BaseModel):
    """The response from the tool to the AI intern."""

    thread_id: str
    tool_results: list[ToolResult]


class EditResult(BaseModel):
    """The result of an edit."""

    thread_id: str
    diff: str
    accepted: bool


# Tools mapping to human readable names
TOOLS_HR_NAMES = {
    ast_utils.get_module_source.__name__: "Analyzing code",
    codegen.add_python_element.__name__: "Adding new elements",
    codegen.update_python_element.__name__: "Updating elements",
    codegen.delete_python_element.__name__: "Deleting elements",
}

FLEXGEN_BACKEND_URL = os.getenv("FLEXGEN_BACKEND_URL", "http://localhost:8000")


class Diff(rx.Base):
    """A diff between two files (before and after)."""

    # The name of the file
    filename: str

    # The diff of the file
    diff: str


@dataclasses.dataclass()
class LocalAgent:
    """The local agent instance."""

    # The remote backend URL.
    backend_url: str = FLEXGEN_BACKEND_URL

    # The agent instance.
    agent = Agent(
        tools=[
            ast_utils.get_module_source,
            codegen.add_python_element,
            codegen.update_python_element,
            codegen.delete_python_element,
        ],
    )

    @staticmethod
    def authorization_header(token: str) -> dict[str, str]:
        """Construct an authorization header with the specified token as bearer token.

        Args:
            token: The access token to use.

        Returns:
            The authorization header in dict format.
        """
        return {"Authorization": f"Bearer {token}"}

    async def make_request(
        self,
        endpoint: str,
        data: dict,
        timeout: int = 60,
    ) -> dict:
        """Make a request to the backend.

        Args:
            endpoint: The endpoint to send the request to.
            data: The data to send.
            timeout: The timeout for the request.

        Returns:
            The JSON response from the backend.
        """

        token, validated_info = hosting.authenticated_token()
        headers = self.authorization_header(token)

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.backend_url}/api/{endpoint}",
                data=data,
                headers=headers,
                timeout=timeout,
            )

        resp.raise_for_status()
        return resp.json()

    async def process(self, request: InternRequest):
        """Process the request from the AI intern.

        Args:
            request: The request from the AI intern.

        Yields:
            The tool use messages from the intern.
        """
        # Create the initial edit request and yield the edit id.
        response = InternResponse(
            **await self.make_request("intern", request.model_dump_json())
        )
        yield response

        # Process and yield the tool use messages.
        while True:
            tool_results: list[ToolResult] = []

            for tool_call in response.tool_calls:
                yield tool_call
                tool_result = await self.agent.invoke_tool(tool_call)
                assert tool_result.tool_call_id == tool_call.id
                tool_result = await self._handle_tool_result(
                    tool_result, tool_call, request
                )
                assert tool_result.tool_call_id == tool_call.id
                tool_results.append(tool_result)

            tool_response_request = ToolRequestResponse(
                thread_id=response.thread_id,
                tool_results=tool_results,
            )

            response = InternResponse(
                **await self.make_request(
                    "intern/tool_response", tool_response_request.model_dump_json()
                )
            )

            # Check if the response is the final response.
            yield response

    async def _handle_tool_result(
        self, tool_result: ToolResult, tool_call: ToolCall, request
    ):
        """Handle the tool response.

        Args:
            tool_result: The result from the tool.
            tool_call: The tool call item.
            request: The original request.

        Returns:
            The processed tool response.
        """
        if not tool_result.is_error and tool_call.name in [
            codegen.add_python_element.__name__,
            codegen.update_python_element.__name__,
            codegen.delete_python_element.__name__,
        ]:
            # The tool is trying to update the source code.
            # Obtain the new source code, from the diff
            suggested_ndiff = tool_result.result
            new_source = "".join(difflib.restore(suggested_ndiff, 2))
            new_source = path_utils.convert_from_scratch_code(
                paths.base_paths[0].name, new_source
            )

            # Obtain the file that the modified module lives in (within the main directory)
            module_modified = "tmp" + tool_call.input["module_name"]
            modified_filename = importlib.util.find_spec(module_modified).origin
            modified_filename = modified_filename.replace(
                str(paths.tmp_root_path), str(paths.base_paths[0].parent)
            )
            try:
                # Obtain the validation function (i.e. index) and the file (in the main directory) where it lives
                main_directory_validation_page = request.parent_component["function"]
                main_directory_validation_file = request.parent_component[
                    "filename"
                ].replace(str(paths.tmp_root_path), str(paths.base_paths[0].parent))
                # Validate the new source
                path_utils.validate_source(
                    new_source,
                    modified_filename,
                    main_directory_validation_page,
                    main_directory_validation_file,
                )
            except Exception as e:
                # This code has failed: return the error message
                tool_result = ToolResult(
                    tool_call_id=tool_result.tool_call_id,
                    result=e.stderr,
                    execution_time=0,
                    is_error=True,
                )
            else:
                # This code has passed: write it into the correct file within the * scratch directory *
                write_to = modified_filename.replace(
                    str(paths.base_paths[0].parent), str(paths.tmp_root_path)
                )
                with open(write_to, "w") as file:
                    new_source = path_utils.convert_to_scratch_code(
                        paths.base_paths[0].name, new_source
                    )
                    content = path_utils.format_code(new_source)
                    file.write(content)
                tool_result = ToolResult(
                    tool_call_id=tool_result.tool_call_id,
                    result=codegen.to_unified_diff(suggested_ndiff),
                    execution_time=tool_result.execution_time,
                )

        console.info("\n\n\n")
        console.info(tool_result)
        console.info("\n\n\n")
        return tool_result

    async def confirm_change(self, thread_id: str, diffs: list[Diff], accepted: bool):
        """Accept or reject the change.

        Args:
            thread_id: The thread ID.
            diffs: The diffs to accept or reject.
            accepted: Whether the change is accepted or rejected.
        """
        console.info(f"Confirming change for {thread_id} (accepted: {accepted})")
        await self.make_request(
            "intern/edit_result",
            data=EditResult(
                thread_id=thread_id,
                diff=json.dumps([d.dict() for d in diffs]),
                accepted=accepted,
            ).model_dump_json(),
        )

        if accepted:
            path_utils.commit_scratch_dir(
                paths.base_paths[0], [d.filename for d in diffs]
            )
        else:
            path_utils.create_scratch_dir(paths.base_paths[0], overwrite=True)

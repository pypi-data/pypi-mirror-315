import json

from pathlib import Path
import reflex as rx

from reflex_ai.utils import path_utils


class RunTimeState(rx.State):
    """Perform some actions on app startup."""

    # track the last reflex run time.
    last_reflex_run_time: rx.LocalStorage

    async def reset_scratch_dir(self, base_path):
        """Reset the scratch directory on every reflex run.

        Args:
            base_path: The root path of the client working dir.
        """
        web_path = Path(base_path).parent / ".web" / "reflex.json"

        with open(web_path) as f:
            data = json.load(f)

        last_reflex_run_time = data.get("last_reflex_run_datetime", "_")

        if not self.last_reflex_run_time == last_reflex_run_time:
            path_utils.create_scratch_dir(Path(base_path), overwrite=True)
            self.last_reflex_run_time = last_reflex_run_time

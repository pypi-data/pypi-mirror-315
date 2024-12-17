import builtins
from importlib.util import find_spec
import os
import sys
import types


def noop(*args):
    """A no-op function.

    Args:
        *args: The arguments to ignore
    """
    pass


original_import = builtins.__import__


def get_custom_import(modified_file, new_source_code_file):
    """Get a custom import function that disables reflex_ai.enable,
    and replaces imports of the modified file the code living in new_source_code_file.

    Args:
        modified_file: The name of the modified file.
        new_source_code_file: The new source code file where the changes are made.

    Returns:
        The custom import function.
    """

    def custom_import(name, globals=None, locals=None, fromlist=(), level=0) -> object:
        """A custom import to disable reflex_ai.enable.

        Args:
            name: The name of the module to import.
            globals: The global namespace.
            locals: The local namespace.
            fromlist: The list of names to import.
            level: The level in the package hierarchy.

        Returns:
            The imported module.
        """

        # Try to find a spec for this name we are importing.
        # Note: Sometimes this will raise an exception, generally we don't care why (we only care if a spec exists, and it corresponds to the file we modified).
        try:
            spec = find_spec(name)
        except Exception:
            spec = None

        if spec is not None and spec.origin == modified_file:
            new_module = types.ModuleType(name)
            with open(new_source_code_file, "r") as f:
                new_source = f.read()
            exec(new_source, new_module.__dict__)
            return new_module

        module = original_import(name, globals, locals, fromlist, level)

        # Disable reflex_ai.enable
        if name == "reflex_ai" and fromlist and "enable" in fromlist:
            module.enable = noop
        return module

    return custom_import


def validate_source(
    new_source_code_file: str,
    modified_file: str,
    validation_function: str,
    validation_file: str,
):
    """Validate the source code by running the validation function.

    Args:
        new_source_code_file: The new source code file where the changes are made.
        modified_file: The name of the modified file.
        validation_function: The validation function to run.
        validation_file: The file containing the validation function.

    Raises:
        Exception: If the code being validated raises an exception.
    """
    builtins.__import__ = get_custom_import(modified_file, new_source_code_file)
    try:
        # Read the source code
        file_with_source_to_exec = (
            new_source_code_file
            if modified_file == validation_file
            else validation_file
        )

        with open(file_with_source_to_exec) as f:
            source_to_exec = f.read()

        # Add the current directory to the path.
        if os.getcwd() not in sys.path:
            sys.path.append(os.getcwd())

        env = {}
        try:
            # Execute the source code.
            exec(source_to_exec, env, env)

            # Run the validation function.
            component_fn = env[validation_function]

            eval(f"{component_fn.__name__}()", env, env)

        except Exception as e:
            print(str(e), file=sys.stderr)
            raise

    finally:
        builtins.__import__ = original_import


if __name__ == "__main__":
    validate_source(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

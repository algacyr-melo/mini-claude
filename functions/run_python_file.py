import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.realpath(os.path.abspath(working_directory))
    abs_file_path = os.path.realpath(os.path.abspath(os.path.join(working_directory, file_path)))

    if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["python", abs_file_path, *(args or [])]
        completed = subprocess.run(
            command,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = []
    if completed.stdout:
        output.append(f"STDOUT:\n{completed.stdout}")
    if completed.stderr:
        output.append(f"STDERR:\n{completed.stderr}")

    if completed.returncode != 0:
        output.append(f"Process exited with code {completed.returncode}")

    return "\n".join(output) if output else "No output produced"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file."
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)


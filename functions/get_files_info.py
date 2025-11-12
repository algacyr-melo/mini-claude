import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.realpath(os.path.abspath(working_directory))
    target_dir = os.path.realpath(os.path.abspath(os.path.join(working_directory, directory)))

    if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        entries_info = []
        for entry in sorted(os.listdir(target_dir)):
            path = os.path.join(target_dir, entry)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            entries_info.append(
                f"- {entry}: file_size={size} bytes, is_dir={is_dir}"
            )
        return "\n".join(entries_info)
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


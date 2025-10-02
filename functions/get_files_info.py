import os


def get_files_info(working_directory, directory="."):
    base = os.path.realpath(os.path.abspath(working_directory))
    target = os.path.realpath(os.path.abspath(os.path.join(working_directory, directory)))

    if os.path.commonpath([base, target]) != base:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'

    try:
        entries_info = []
        for entry in sorted(os.listdir(target)):
            path = os.path.join(target, entry)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            entries_info.append(
                f"- {entry}: file_size={size} bytes, is_dir={is_dir}"
            )
        return "\n".join(entries_info)
    except Exception as e:
        return f'Error: {e}'


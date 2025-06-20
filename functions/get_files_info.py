import os

from google.genai import types


def get_files_info(working_directory, directory=None):
    if directory:
        full_path = os.path.realpath(os.path.join(working_directory, directory))
        base_path = os.path.realpath(working_directory)
        if not full_path.startswith(base_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        contents = os.listdir(full_path)
        lines = []
        for entry in contents:
            entry_path = os.path.join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            size = os.path.getsize(entry_path)
            lines.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    else:
        return "No directory specified"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
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

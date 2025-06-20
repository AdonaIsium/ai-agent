import os

from google.genai import types


def write_file(working_directory, file_path, content):
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    base_path = os.path.realpath(working_directory)
    if not full_path.startswith(base_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    with open(full_path, "w") as f:
        f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Runs a targetted .py file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path from the working directory to the file we want to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content we want to write into the targetted file",
            ),
        },
    ),
)

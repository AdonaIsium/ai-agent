import os


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

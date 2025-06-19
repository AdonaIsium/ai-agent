import os


def get_file_content(working_directory, file_path):
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    base_path = os.path.realpath(working_directory)
    if not full_path.startswith(base_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(full_path, "r") as f:
        contents = f.read()
        if len(contents) > 10000:
            return (
                f'{contents[:10001]}...File "{file_path}" truncated at 10000 characters'
            )
        else:
            return contents

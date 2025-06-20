import os
import subprocess


def run_python_file(working_directory, file_path):
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    base_path = os.path.realpath(working_directory)

    if not full_path.startswith(base_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", full_path], capture_output=True, text=True, timeout=30
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output.append(f"Exit code: {result.returncode}")
        return "\n".join(output) or "Execution completed with no output."

    except subprocess.TimeoutExpired as e:
        return f"Error: Execution timed out after {e.timeout} seconds."

    except Exception as e:
        return f"Error: Failed to execute Python file: {e}"

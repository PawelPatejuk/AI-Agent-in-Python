import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    if (args is None):
        args = []
        
    try:
        full_path = os.path.join(working_directory, file_path)
    except:
        return f"Error: Cannot create path from '{working_directory}' and '{file_path}'"

    try:
        if (not os.path.abspath(full_path).startswith(os.path.abspath(working_directory))):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except:
        return f'Error: Cannot check is if "{file_path}" is outside the permitted "{working_directory}" working directory'

    try:
        if (not os.path.exists(full_path)):
            return f'Error: File "{file_path}" not found.'
    except:
        return f"Error: Cannot check if file '{full_path}' exists"

    try:
        if (not full_path.endswith(".py")):
            return f'Error: "{file_path}" is not a Python file.'
    except:
        return f"Error: Cannot check file '{full_path}' extension"     

    try:
        completed_process = subprocess.run(["python3", file_path], cwd=working_directory, timeout=30, capture_output=True, text=True)

        if (completed_process.returncode):
            return f"Process exited with code {completed_process.returncode}"
        if (not completed_process.stdout and not completed_process.stderr):
            return "No output produced."
        
        return f"STDOUT: {completed_process.stdout}STDERR: {completed_process.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file with optional command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

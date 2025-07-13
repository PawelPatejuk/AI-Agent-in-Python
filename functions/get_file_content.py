import os

from google.genai import types

from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
    except:
        return f"Error: Cannot combine '{working_directory}' and '{file_path}' path"

    if (not os.path.abspath(full_path).startswith(os.path.abspath(working_directory))):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    if (not os.path.isfile(full_path)):
        return f"Error: '{file_path}' is not a file"
    
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if (f.read(1)):
                file_content_string += '...File "{file_path}" truncated at 10000 characters' 
    except:
        return f"Error: Cannot read '{file_path}' file"
    
    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

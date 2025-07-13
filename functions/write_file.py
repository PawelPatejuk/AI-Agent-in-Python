import os

from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
    except:
        return f"Error: Cannot combine path from '{working_directory}' and '{file_path}'"
    
    if (not os.path.abspath(full_path).startswith(os.path.abspath(working_directory))):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, "w") as f:
                try:
                    f.write(content)
                except:
                    return f"Error: Cannot write to '{full_path}' path"
        except:
            return f"Error: Cannot open '{full_path}' path"
    except:
        return f"Error: Cannot create '{full_path}' path"

    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite content to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

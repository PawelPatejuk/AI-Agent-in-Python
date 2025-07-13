import os

from google.genai import types

def get_files_info(working_directory, directory=None):    
    directory = directory if directory else "."

    try:
        full_path = os.path.join(working_directory, directory)
    except:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    if (not abs_full_path.startswith(abs_working_dir)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if (not os.path.isdir(full_path)):
        return f'Error: "{directory}" is not a directory'

    try:
        contents = os.listdir(full_path)
    except:
        return f'Error: Cannot list "{directory}"'

    lines = [f"Result for {'current' if directory == '.' else directory} directory:"]
    
    for file in contents:
        file_full_path = os.path.join(full_path, file)
        
        try:
            size = os.path.getsize(file_full_path)
        except:
            return f"Error: unknown size"

        try:
            is_dir = os.path.isdir(file_full_path)
        except:
            return f"Error: unknown type"
        
        lines.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")


    return "\n".join(lines)


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

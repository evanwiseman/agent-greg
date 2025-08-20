import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes file content in the specified file path along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to write content, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.TYPE_UNSPECIFIED,
                description="The content to write into the file."
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_full_path.startswith(abs_working_directory):
        raise PermissionError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    os.makedirs(os.path.dirname(abs_full_path), exist_ok=True)
    
    with open(abs_full_path, "w") as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
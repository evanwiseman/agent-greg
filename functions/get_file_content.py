import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file content in the specified file path along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to retreive its content, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_full_path.startswith(abs_working_directory):
        raise PermissionError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    
    if not os.path.isfile(abs_full_path):
        raise FileNotFoundError(f'Error: File not found or is not a regular file: "{file_path}"')
    
    with open(abs_full_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
    
    return file_content_string
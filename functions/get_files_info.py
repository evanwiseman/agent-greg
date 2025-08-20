import os
from google.genai import types

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

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(os.path.join(working_directory, directory))
    
    if not abs_full_path.startswith(abs_working_directory):
        raise PermissionError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if not os.path.exists(abs_full_path):
        raise FileNotFoundError(f'Error: "{directory}" is not a directory')
    
    files_content = []
    with os.scandir(abs_full_path) as entries:
        for entry in entries:
            entry_stats = entry.stat()
            content = f"- {entry.name}: file_size={entry_stats.st_size}, is_dir={entry.is_dir()}"
            files_content.append(content)
    return "\n".join(files_content)
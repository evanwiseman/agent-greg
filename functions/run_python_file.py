import os
import sys
import subprocess
from typing import List
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file at the specified file path with the specified arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to retreive its content, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The arguments to pass into the python executable. If not provided, the file will run with no args."
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args:List[str]=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_full_path.startswith(abs_working_directory):
        raise PermissionError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    
    if not os.path.isfile(abs_full_path):
        raise FileNotFoundError(f'Error: File "{file_path}" not found.')

    if not abs_full_path.endswith(".py"):
        raise ValueError(f'Error: "{file_path}" is not a Python file.')
    
    try:
        completed_process = subprocess.run(
            args=[sys.executable, abs_full_path, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=abs_working_directory,
            timeout=30
        )
        
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()
        output_parts = []
        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")
            
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
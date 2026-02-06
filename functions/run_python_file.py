import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file in a specified directory relative to the working directory, with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Extra arguments to pass to the python file",
                items=types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(
                        type=types.Type.STRING
                    )
                ),
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)    
    target_file_abs =  os.path.abspath(os.path.join(working_directory,file_path))
    try:
        if os.path.commonpath([working_dir_abs, os.path.commonpath([working_dir_abs, target_file_abs])]) == working_dir_abs:
            if os.path.isfile(target_file_abs):
                    filename = os.path.splitext(file_path)
                    filename_ext = filename[1]
                    if filename_ext == ".py":
                        command = ["python3", target_file_abs]
                        if args is not None:
                            for arg in args:    
                                command.extend(arg)
                        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
                        if result.returncode != 0:
                            return f"Process exited with code {result.returncode}"
                        elif not result.stdout and not result.stderr:
                            return "No output produced"
                        else:
                            return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
                    else:
                        return f'Error: "{file_path}" is not a Python file'
            else:
                return f'Error: "{file_path}" does not exist or is not a regular file'
        else:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: executing Python file: {e}" 
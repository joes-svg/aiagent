import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists contents of a file in a specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to list contents of, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)    
        target_file_abs =  os.path.abspath(os.path.join(working_directory,file_path))
        if os.path.commonpath([working_dir_abs, os.path.commonpath([working_dir_abs, target_file_abs])]) == working_dir_abs:
            if os.path.isfile(target_file_abs):
                file = open(target_file_abs)
                content = file.read(10000)
                if file.read(1):
                    content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return content    
            else:
                return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        print(f"Error: {type(e)} - {str(e)}")    
        
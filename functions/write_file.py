import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file in a specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write in a specified directory relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)    
        target_file_abs =  os.path.abspath(os.path.join(working_directory,file_path))
        if os.path.commonpath([working_dir_abs, os.path.commonpath([working_dir_abs, target_file_abs])]) == working_dir_abs:
            if not os.path.isdir(target_file_abs):
                os.makedirs(working_dir_abs, exist_ok=True)
                file = open(target_file_abs, 'w')
                file.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            else:
                return f'Error: Cannot write to "{file_path}" as it is a directory'
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        print(f"Error: {type(e)} - {str(e)}") 
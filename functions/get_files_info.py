import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        contents = ""
      
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        valid_path = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    
        if valid_path:
            dir_contents = os.listdir(target_dir)
            for item in dir_contents:
                contents += f"- {item}: {os.path.getsize(os.path.join(target_dir,item))} bytes, is_dir={ os.path.isdir(os.path.join(target_dir,item))} \n"
            return contents
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        print(f"Error: {type(e)} - {str(e)}")    
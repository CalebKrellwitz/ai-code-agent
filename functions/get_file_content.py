import os

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not os.path.isdir(abs_working_directory):
        return f'Error: "{working_directory}" is not a directory'
    elif not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    file_content_string = ""

    with open(abs_file_path, "r") as f:
        file_content_string = f.read(10000)

    if len(file_content_string) == 10000:
        file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string

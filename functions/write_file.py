import os

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not os.path.isdir(abs_working_directory):
        return f'Error: "{working_directory}" is not a directory'
    elif not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.isdir(os.path.dirname(abs_file_path)):
        os.makedirs(os.path.dirname(abs_file_path))

    with open(abs_file_path, 'w') as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

import os

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    # debugging
    #print(f"abs_working_directory={abs_working_directory}\nabs_directory={abs_directory}")
    
    if not os.path.isdir(abs_working_directory):
        return f'Error: "{working_directory}" is not a directory'
    elif not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    elif not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    dir_contents = os.listdir(path=abs_directory)
    files_info = []

    for name in dir_contents:
        name_path = os.path.join(abs_directory, name)
        files_info.append(
            "- " + str(name) + ': ' +
            "file_size=" + str(os.path.getsize(name_path)) + " bytes, " +
            "is_dir=" + str(os.path.isdir(name_path))
        )

    return '\n'.join(files_info)

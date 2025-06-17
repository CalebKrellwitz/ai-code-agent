import os
from google import genai

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory)) if directory != None else abs_working_directory
    
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

schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

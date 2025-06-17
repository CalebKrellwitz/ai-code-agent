import os
from google import genai

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

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the content of the file at the specified file path, constrained to the working directory. If the file does not exist, it will be created.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The path to the file to be written or overwritten, relative to the working directory.",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The content with which to write or overwrite the specified file.",
            ),
        },
    ),
)

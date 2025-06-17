import os
from google import genai

from config import MAX_CHARS

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
        file_content_string = f.read(MAX_CHARS)

    if len(file_content_string) == MAX_CHARS:
        file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    return file_content_string
  
schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of the file at the specified file path, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The path to the file to read content from, relative to the working directory.",
            ),
        },
    ),
)

import os
import sys
from dotenv import load_dotenv
from google import genai

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

client_name = "gemini-2.0-flash-001"
working_directory = "./calculator"
verbose = "--verbose" in sys.argv
user_prompt = sys.argv[1]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Write or overwrite files
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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

schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python script located at the specified file path, constrained to the working directory. Files ending in '.py' are Python scripts.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    args = function_call_part.args.copy()
    args["working_directory"] = working_directory

    function_result = None

    if function_call_part.name == "get_files_info":
        function_result = get_files_info(**args)
    elif function_call_part.name == "get_file_content":
        function_result = get_file_content(**args)
    elif function_call_part.name == "write_file":
        function_result = write_file(**args)
    elif function_call_part.name == "run_python_file":
        function_result = run_python_file(**args)
    else:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return genai.types.Content(
        role="tool",
        parts=[
            genai.types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

messages = [
    genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model=client_name, 
    contents=messages,
    config=genai.types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    ),
)

for function_call_part in response.function_calls:
    function_call_result = call_function(function_call_part, verbose)
    if function_call_result.parts[0].function_response.response == None:
        raise Exception("Error: function called gave no response")
    if verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")

#print(response.text)

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

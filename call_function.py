from google import genai

from config import WORKING_DIRECTORY

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

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
    args["working_directory"] = WORKING_DIRECTORY

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

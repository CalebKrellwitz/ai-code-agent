import os
import sys
from dotenv import load_dotenv
from google import genai

from system_prompt import system_prompt
from call_function import call_function, available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

verbose = "--verbose" in sys.argv
user_prompt = sys.argv[1]

messages = [
    genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
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

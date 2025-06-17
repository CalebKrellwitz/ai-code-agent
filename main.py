import os
import sys
from dotenv import load_dotenv
from google import genai

from config import GEMINI_MODEL, MAX_ITERATIONS
from system_prompt import system_prompt
from call_function import call_function, available_functions

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print('''AI Code Agent\n\nUsage: python3 main.py "your prompt here" [--verbose]\nExample: python3 main.py "How do I fix the calculator?"''')
        sys.exit(1)
        
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = ' '.join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
    ]

    for _ in range(MAX_ITERATIONS):
        response_text = generate_content(client, messages, verbose)
        if isinstance(response_text, str):
            break

    print(response_text)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=GEMINI_MODEL, 
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    for candidate in response.candidates:
        messages.append(candidate.content)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Error: function called gave no response")

        messages.append(function_call_result)

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0].function_response.response)
    
    if not function_responses:
        raise Exception("no function responses generated")

if __name__ == "__main__":
    main()

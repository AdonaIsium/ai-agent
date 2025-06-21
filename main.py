import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iterations = 0
    while True:
        iterations += 1
        if iterations > 20:
            print("Too much loopage, sorry~ Only 20 allowed!")
            sys.exit(1)

        try:
            response = generate_content(client, messages, verbose)
            if response:
                print("Response:")
                print(response)
                break
        except Exception as e:
            print(f"Error found, send help: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],  # Make sure this is defined/imported
            system_instruction=system_prompt,  # Also make sure this is defined/imported
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            content = candidate.content
            messages.append(content)

    if not response.function_calls:
        return response.text or "(No text response from model)"

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose)

        if (
            not function_call_result.parts
            or not hasattr(function_call_result.parts[0], "function_response")
            or not hasattr(function_call_result.parts[0].function_response, "response")
        ):
            raise RuntimeError("Function response missing or malformed")

        function_result_part = function_call_result.parts[0]

        result_data = function_result_part.function_response.response

        if verbose:
            print(f"-> {result_data}")

        function_responses.append(function_result_part)

    if not function_responses:
        raise Exception("No responses generated")

    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()

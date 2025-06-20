import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Gemini Helper")

    parser.add_argument("request", type=str, help="Your request to Gemini")

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Optional verbose mode for debugging",
    )

    args = parser.parse_args()

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    user_request = args.request

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_request)]),
    ]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if args.verbose:
        print(f"User prompt: {user_request}")
        if response.function_calls:
            function_call_part = response.function_calls[0]
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )
        if response.usage_metadata:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)
    else:
        if response.function_calls:
            function_call_part = response.function_calls[0]
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()

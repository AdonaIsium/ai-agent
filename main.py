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

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_request)]),
    ]

    if args.verbose:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
        )
        print(f"User prompt: {user_request}")
        if response.usage_metadata:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)
    else:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
        )
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()

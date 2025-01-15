import openai
import os
from dotenv import load_dotenv

load_dotenv()

gemini_token = os.getenv("GEMINI_TOKEN")    

openai.api_key = 'api_key'

def get_response(prompt, context):
    """Generates a response using Gemini based on the prompt and context.

    Args:
        prompt (str): The user's prompt.
        context (str): Relevant context for the response.

    Returns:
        str: The generated response.
    """

    combined_text = f"User message: {prompt}\n\nContext: {context}"

    response = openai.Completion.create(
        engine="text-davinci-003",  # Replace with your desired Gemini model
        prompt=combined_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response.choices[0].text

get_response("What is the capital of France?", "Context: This is a conversation with a user.")

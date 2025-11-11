import os
import openai
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


# simple wrapper function
async def generate_reply(system_prompt: str, user_message: str):
# Note: openai python client does not have async ChatCompletion out of the box
# For simplicity we'll use synchronous call executed in threadpool if needed
    prompt = f"{system_prompt}\nUser: {user_message}\nAssistant:"
    res = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=300,
    temperature=0.7,
    )
    return res.choices[0].text.strip()
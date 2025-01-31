from openai import OpenAI
from models.meetings import Meetings
import os

openai_key = os.environ.get('OPENAI_API_KEY')

def parse_with_model(parse_description):
    client = OpenAI(
        api_key=openai_key
    )

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Extract list of meetings from the text."},
            {"role": "user", "content": parse_description},
        ],
        response_format=Meetings
    )

    return completion.choices[0].message.parsed
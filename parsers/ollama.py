from ollama import chat
from models.meetings import Meetings

parse_description = """
    Parse the above data into a list of Meeting objects using the specified Meetings model.  Meetings is a list of Meeting objects
    which will have at least one or all of these properties.  Name will always be present as the first line of the entry, however phone number
    or URL may be absent.  In some cases meetings may have more than one phone number.

    1.  name:
    2.  address:
    3.  url:
    4.  phoneNumber:
"""

def parse_with_model(content):
    print(len(content + parse_description))
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': content + "\n" + parse_description,
            }
        ],
        model='deepseek-r1:latest',
        options={
            'num_ctx': 4096
        },
        format=Meetings.model_json_schema()
    )

    meetings = Meetings.model_validate_json(response.message.content)
    return meetings
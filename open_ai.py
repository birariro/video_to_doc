from openai import OpenAI

from prompt import get_prompt


def request_summery(api_key, model_type, video_script):
    client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
    messages = [
        {
            "role": "system",
            "content": (
                get_prompt()
            ),
        },
        {
            "role": "user",
            "content": video_script,
        },
    ]

    return client.chat.completions.create(
        model=model_type,
        messages=messages,
    )

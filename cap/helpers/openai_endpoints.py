import os
import openai
from openai import OpenAI

# RIPL one
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

gpt_config = {
    'stop': ['# '],
    'temperature': 0,
    'max_tokens': 256
}


def call_gpt35(model, prompt, stop, temperature, max_tokens, report_usage=False):
    print('Calling OpenAI API...')
    api_results = client.completions.create(
        model=model,
        prompt=prompt,
        stop=stop,
        temperature=temperature,
        max_tokens=max_tokens
    )
    if report_usage:
        print('%%%%%% token usage %%%%%%')
        print(api_results.usage)
        print('%%%%%%%%%%%%')
    return api_results.choices[0].text.strip()


def call_gpt4(prompt, stop, temperature, max_tokens, report_usage=False):
    # NOTE: This may be broken
    print('Calling GPT-4 API...')
    api_results = client.chat.completions.create(model='gpt-4',
                                                 stop=stop,
                                                 temperature=temperature,
                                                 max_tokens=max_tokens,
                                                 messages=[
                                                     {'role': 'user', "content": prompt},
                                                 ])
    if report_usage:
        print('%%%%%% token usage %%%%%%')
        print(api_results.usage)
        print('%%%%%%%%%%%%')
    return api_results.choices[0].message.content


def call_api(model, prompt, stop=gpt_config['stop'], temperature=gpt_config['temperature'], max_tokens=gpt_config['max_tokens'], report_usage=False):
    """A wrapper to retry calling the API in the case of RateLimitError."""
    success = False
    while not success:
        try:
            return call_gpt35(model, prompt, stop, temperature, max_tokens, report_usage=report_usage)
            # if engine == 'text-davinci-003':
            #     return call_gpt35(prompt, stop, temperature, max_tokens, report_usage=report_usage)
            # elif engine == 'gpt-4':
            #     return call_gpt4(prompt, stop, temperature, max_tokens, report_usage=report_usage)
            # else:
            #     raise ValueError(f"Unknown engine {engine}")
            success = True
        except openai.RateLimitError as e:
            print(f"!!!! Captured: {e}")
            print('Retrying in 15 seconds...')
            import time
            time.sleep(15)

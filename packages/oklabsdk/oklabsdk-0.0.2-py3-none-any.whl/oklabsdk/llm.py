import os
import requests # type: ignore
from openai import OpenAI

api_key = os.getenv("API_KEY")
endpoint = os.getenv("API_ENDPOINT")
deployment_name = os.getenv("DEPLOYMENT_NAME")


model = OpenAI(api_key, base_url=endpoint)

def get_response(prompt, max_tokens=4000):   
    """Returns the response from the LLM model. High time consumption."""
    url =  f"{endpoint}chat/completions"
    headers = {"Content-Type": "application/json","Authorization": f"Bearer {api_key}"}
    data = {"model": deployment_name,"messages": [{"role": "user", "content": prompt}],"temperature": 0.7}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # Vrátí obsah odpovědi
        return response.json()['choices'][0]['message']['content']
    else:
        # throw an error
        response.raise_for_status()
        return None
    
    
def get_completion(prompt):
    """Returns the completion from the LLM model. High time consumption."""
    completion = model.completions.create(model=deployment_name, messages=[{"role": "user", "content": prompt}])
    return completion
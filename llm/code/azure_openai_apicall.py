# code/azure_openai_apicall.py
import json
import os
import openai
import backoff
from langchain import PromptTemplate, LLMChain
from langchain.llms import AzureOpenAI

class AzureOpenAIApiCall:
    def __init__(self, temperature=0):
        self.temperature = temperature

    def run(self, text):
        myArticle = text
        myJson = "{\"Crisis_Yes_No\": \"Yes\",\"Category\": \"\",\"Summary\": \"\",\"Why_A_Crisis\": \"\",\"Locations\": [],\"Number of People Affected\": \"\"}"
        article = myArticle[:1500]
        myArticle = article
        xjson = myJson
        prompt_text = "Evaluate if this is a humanitarian crisis from the following news article. If no, reply with no and do not summarize. If yes, provide a summary of the article in less than 100 words. If yes, state why it's a humanitarian crisis. If yes, create a 1 to 3 word category. Put your reponse in the following JSON structure: ### {xjson} ### ### news article: ### {article} ###"
        prompt = prompt_text.format(xjson=myJson, article=myArticle)


        response = call_openai(prompt)
        
        result = response["choices"][0]["text"]
        json_data = fix_json(result)
    
        return json_data

def backoff_hdlr(details):
    print ("Backing off {wait:0.1f} seconds after {tries} tries "
           "calling function {target} with args {args} and kwargs "
           "{kwargs}".format(**details))

#@backoff.on_exception(backoff.expo, openai.OpenAIError, max_time=1800, on_backoff=backoff_hdlr)
def call_openai(prompt):
    return openai.Completion.create(
        engine="text-davinci-003",
        temperature=0,
        prompt=prompt,
        max_tokens=2048
    )

def fix_json(json_str):
    try:
        return json.loads(json_str)
    except ValueError as e:
        try:
            # Find the position of the first error in the string
            pos = e.args[1]
            # Attempt to fix the JSON string
            if json_str[pos-1] == ',':
                # Remove the trailing comma
                fixed_json = json_str[:pos-1] + json_str[pos:]
            else:
                # Add a missing closing brace or bracket
                brace = {'{': '}', '[': ']'}
                last_open = [i for i, c in enumerate(json_str[:pos]) if c in brace.keys()][-1]
                missing = brace[json_str[last_open]]
                fixed_json = json_str[:pos] + missing + json_str[pos:]
            # Retry with the fixed JSON string
        except IndexError:
            # If we can't find the position of the error, just return an empty json string
            return json_str
           
        return fix_json(fixed_json)
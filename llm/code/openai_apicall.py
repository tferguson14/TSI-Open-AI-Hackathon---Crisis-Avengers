# code/openai_apicall.py
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
import json

class OpenAIApiCall:
    def __init__(self, temperature=0):
        self.temperature = temperature

    def run(self, text):
        myArticle = f"{text}\n\n"
        myJson = "{\"Crisis_Yes_No\": \"Yes\",\"Summary\": \"\",\"Why_A_Crisis\": \"\",\"Locations\": [],\"Number of People Affected\": \"\"}"

        template = "Evaluate if this is a humanitarian crisis from the following news article. If no, reply with no and do not summarize. If yes, provide less than 100 word or less summary of the article. If yes, state why it's a humanitarian crisis. Put your reponse in the following JSON structure: ### {json} ### ### news article: ### {article} ###"
        prompt = PromptTemplate(template=template, input_variables=["json", "article"])
        
        llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=self.temperature))
        result = llm_chain.run(json=myJson, article=myArticle)

        json_data = fix_json(result)
        return json_data


def fix_json(json_str):
    try:
        return json.loads(json_str)
    except ValueError as e:
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
        return fix_json(fixed_json)
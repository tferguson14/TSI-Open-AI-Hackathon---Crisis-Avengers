# project/code/tsi_hackathon.py
# export OPENAI_API_KEY=sk

import json
import time
import openai
from data_preperation import DataProcessor
from openai_apicall import OpenAIApiCall
from azure_openai_apicall import AzureOpenAIApiCall

# define the files
data_file = 'files/eventsdata_sample_text_5k.json'
ids_to_skip_file = 'files/ids_to_skip.txt'
results_file = 'files/results.json'

# define the dictionary of keywords
keywords = {
    "natural_disaster": ["earthquake", "tsunami", "hurricane", "flood", "drought"],
    "conflict_displacement": ["armed conflict", "civil war", "displacement", "refugee", "migrant"],
    "epidemic_and_pandemic": ["outbreak", "disease", "ebola", "zika", "cholera", "measles", "malaria", "flu", "pandemic", "epidemic"],
    "food_insecurity_malnutrition": ["hunger", "starvation", "malnutrition", "food insecurity", "food security", "food crisis", "food shortage", "food aid", "food assistance", "food distribution"],
    "refugee_asylum_seeker": ["forced", "flee", "persecution", "conflict", "violence", "displacement", "refugee", "migrant", "asylum seeker", "asylum", "migration", "migrants", "refugees", "displaced", "displaced persons"],
    "gender-based_violence": ["sexual assault", "domestic violence"],
    "water_sanitation": ["sanitation", "water", "water shortage", "water crisis", "water contamination", "water pollution", "water access", "water supply", "water treatment", "water quality", "water scarcity"],
    "human_rights_abuses_violation": ["torture", "forced", "exploitation", "abuse", "violence", "persecution", "conflict", "displacement"],
    "environmental_degradation_climate_change": ["climate", "drought", "flood","crisis", "disaster", "emergency", "emergency response"]
}

# create a data processor instance and prepare the items
data_processor = DataProcessor(data_file, keywords, ids_to_skip_file)
prepped_items = data_processor.prep_items()

# create a single instance of the ApiCall class
#api_call = OpenAIApiCall()
api_call = AzureOpenAIApiCall()

# print the results
print("Matching items:")
for item in prepped_items:
    print(f"- {item['_c0']}: {item['keyword']} ({item['Text'][:25]})")

with open(ids_to_skip_file, 'a') as skip_output_file, open(results_file, 'a') as result_output_file:
    ii = 0
    for item in prepped_items:
        ii += 1
        print(f"Processing item {ii} of {len(prepped_items)} for id {item['_c0']}")
        #if ii == 10:
        #    break

        try:
            # *** call API ****
            openai_result = api_call.run(text=item["Text"])

            # add the _c0 value to the openai_result     
            json_result = {"_c0": item["_c0"], "json_result": openai_result}
            print(json_result)

            # write the _c0 value to the ids_to_skip_file if it's not a humanitarian crisis
            if "Crisis_Yes_No" in json_result and json_result["Crisis_Yes_No"] == "No":
                skip_output_file.write(str(item["_c0"]) + '\n')

            result_output_file.write(json.dumps(json_result) + '\n')
                
        # write the openai_result to the result_file
        except openai.OpenAIError as e:
            if e.code == "content_filter":
                print(f"- {item['_c0']}: Content filter error")
                json_result = {"_c0": item["_c0"], "json_result": str(e)}
                skip_output_file.write(str(item["_c0"]) + '\n')
                result_output_file.write(json.dumps(json_result) + '\n')
            else:
                print("Error: " + str(e))
            continue

        time.sleep(2) # optional delay to avoid rate limiting
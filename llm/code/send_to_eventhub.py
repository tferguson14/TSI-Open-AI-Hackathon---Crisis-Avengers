import json
import time
from azure.eventhub import EventHubProducerClient, EventData
# with open("files/results5k.json", "r") as file:
# Replace connection string and event hub name with your own values
CONNECTION_STR = "Endpoint=sb://xxxxxxx.servicebus.windows.net/;SharedAccessKeyName=xxxxxx;SharedAccessKey=xxxxxxxxx;EntityPath=xxxxxx-eaus"
EVENT_HUB_NAME = ""

# Define function to send event data to Azure Event Hub
def send_event(event_data):
    producer = EventHubProducerClient.from_connection_string(CONNECTION_STR, event_hub_name=EVENT_HUB_NAME)
    with producer:
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(event_data))
        producer.send_batch(event_data_batch)
    
    
# Read the JSONL file
with open("files/results5k.json", "r") as file:
    for line in file:
        try:
            row = json.loads(line)
            if isinstance(row, dict) and "json_result" in row and isinstance(row["json_result"], dict) and "Crisis_Yes_No" in row["json_result"] and row["json_result"]["Crisis_Yes_No"] == "Yes":
                send_event(line.strip().encode("utf-8"))
            else:
                print(f"Invalid JSON object: {line}")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        time.sleep(1/10)  # Wait before sending the next event

import csv
import json

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
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
     
    # Open a CSV file to write the data
    with open('csvFilePath', 'w', newline='') as csv_file:
        # Create a CSV writer
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow(['_c0', 'Crisis_Yes_No', 'Category', 'Summary', 'Why_A_Crisis', 'Locations', 'Number of People Affected'])

        # Write the data rows
        for item in data:
            row = [item['_c0']]
            json_data = item['json_result']
            row.append(json_data.get('Crisis_Yes_No', ''))
            row.append(json_data.get('Category', ''))
            row.append(json_data.get('Summary', ''))
            row.append(json_data.get('Why_A_Crisis', ''))
            row.append(', '.join(json_data.get('Locations', [])))
            row.append(json_data.get('Number of People Affected', ''))
            writer.writerow(row)
# Function to convert a JSON to CSV
# Takes the file paths as arguments

def jsonl_to_csv(jsonl_file_path, csv_file_path):
    with open(jsonl_file_path, 'r') as jsonl_file, open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['_c0', 'Crisis_Yes_No', 'Category', 'Summary', 'Why_A_Crisis', 'Locations', 'Number of People Affected']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for line in jsonl_file:
            try:
                json_data = json.loads(line)
            except json.JSONDecodeError:
                print(f"Skipping line (invalid JSON): {line}")
                continue

            if not isinstance(json_data, dict):
                print(f"Skipping line (not a dictionary): {line}")
                continue

            json_result = json_data.get('json_result', {})
            if not isinstance(json_result, dict):
                print(f"Skipping line (json_result not a dictionary): {line}")
                continue

            writer.writerow({
                '_c0': json_data.get('_c0', ''),
                'Crisis_Yes_No': json_result.get('Crisis_Yes_No', ''),
                'Category': json_result.get('Category', ''),
                'Summary': json_result.get('Summary', ''),
                'Why_A_Crisis': json_result.get('Why_A_Crisis', ''),
                'Locations': ', '.join(json_result.get('Locations', [])),
                'Number of People Affected': json_result.get('Number of People Affected', '')
            })

# Driver Code
 
# Decide the two file paths according to your
# computer system
jsonFilePath = r'files/results5k_part1.json'
csvFilePath = r'files/results5k_part1.csv'

# Call the make_json function
jsonl_to_csv(jsonFilePath, csvFilePath)


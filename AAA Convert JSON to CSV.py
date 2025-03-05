import json
import csv

def json_to_csv(json_file_path, csv_file_path):
    # Read JSON data with utf-8 encoding
    json_file_path = input("What's the JSON you are trying to convert called? ")
    json_file_path += ".json"
    name = json_file_path
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Open CSV file for writing with utf-8 encoding
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        # Create CSV writer
        writer = csv.writer(csv_file)
        
        # Write headers
        if isinstance(data, list):
            headers = data[0].keys()
            writer.writerow(headers)
        
            # Write data rows
            for item in data:
                writer.writerow(item.values())
        else:
            headers = data.keys()
            writer.writerow(headers)
            writer.writerow(data.values())

    print(f"Data successfully written to {csv_file_path}")

# Example usage
json_file_path = 'input.json'
csv_file_path = f'output.csv'
json_to_csv(json_file_path, csv_file_path)


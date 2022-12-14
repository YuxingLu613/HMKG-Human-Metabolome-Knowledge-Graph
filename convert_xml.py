import xmltodict
import json


def convert_xml_to_json(input_path, output_path):
    
    with open(input_path, "r") as f:
        xml_data = f.read()
        
    json_data = json.dumps(xmltodict.parse(xml_data),
                           sort_keys=False, indent=2)
    
    with open(output_path, "w") as f:
        f.write(json_data)
    return 

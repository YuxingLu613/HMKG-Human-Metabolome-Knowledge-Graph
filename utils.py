import json


def read_json_file(file_path):
    # Open the file at the specified file path
    with open(file_path, "r") as f:
        # Load the file's content as a JSON object
        json_data = json.load(f)
    
    # Return the JSON data
    return json_data

def check_list(dict):
    # Iterate over each element in the dictionary
    for i in dict:
        # If the current element is a string or a dictionary, skip it
        if isinstance(i, str) or isinstance(i, dict):
            continue
        # If the current element is not a string or a dictionary, return False
        else:
            return False
    # If all elements in the dictionary are either strings or dictionaries, return True
    return True 



def clean_quote(sentence):
    # Removes all instances of the character "'" from the input sentence.
    while "'" in sentence:
        sentence = sentence.replace("'", "")
    return sentence



def drop_duplicate(li):
    # Remove all the duplicate elements
    if isinstance(li[0], str):
        return list(set(li))
    else:
        temp_list = list(set([str(i) for i in li]))
        li = [eval(i) for i in temp_list]
    return li

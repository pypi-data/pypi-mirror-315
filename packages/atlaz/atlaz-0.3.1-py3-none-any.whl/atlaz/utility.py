import json
import tiktoken # type: ignore

def count_tokens(string_inp):
    encc = tiktoken.encoding_for_model("gpt-4")
    encoded_str = encc.encode(string_inp)
    return len(encoded_str)

def read_txt(file_input):
    with open(file_input, 'r') as file:
        data = file.read()
    return data

def write_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_json(json_name):
    with open(json_name, 'r', encoding='utf-8') as f:
        return json.load(f)
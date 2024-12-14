import tiktoken # type: ignore

def count_tokens(string_inp):
    encc = tiktoken.encoding_for_model("gpt-4")
    encoded_str = encc.encode(string_inp)
    return len(encoded_str)

def read_txt(file_input):
    with open(file_input, 'r') as file:
        data = file.read()
    return data
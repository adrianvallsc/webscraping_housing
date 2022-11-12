import  re

def paste_web(*args: str):
    """
    This function takes as input several strings and paste them in the web format

    :param args: strings separated by comma
    :return: string with the pasted elements
    """

    string = "".join([char.lower().strip("/")+"/" for char in args if char != ""])
    return string


def search_text(text, string_search, dict, var_name):

    if re.search(string_search, text):
        dict[var_name] = text
    else:
        dict[var_name] = None

    return dict

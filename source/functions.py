import re


def paste_web(*args: str):
    """
    This function takes as input several strings and paste them in the web format

    :param args: strings separated by comma
    :return: string with the pasted elements
    """

    string = "".join([char.lower().strip("/") + "/" for char in args if char != ""])
    return string


def search_text(text: str, string_search: str, dix: dict, var_name: str) -> dict:

    if re.search(string_search, text):
        if text not in dix:
            dix[var_name] = text
    else:
        if var_name not in dix:
            dix[var_name] = None

    return dix


def parse_list(text, dix: dict, **kwargs) -> dict:

    for k in text:
        item = k.text
        for key, value in kwargs.items():
            dix = search_text(item, value, dix, key)

    return dix

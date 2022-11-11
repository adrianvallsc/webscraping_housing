

def paste_web(*args: str):
    """
    This function takes as input several strings and paste them in the web format

    :param args: strings separated by comma
    :return: string with the pasted elements
    """

    string = "".join([char.lower().strip("/")+"/" for char in args if char != ""])
    return string



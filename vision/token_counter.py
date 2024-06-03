import tiktoken


def count_tokens(string: str, model: str) -> int:
    """
    This function counts the number of tokens in a given string based on the encoding of a specific AI model.

    Args:
        string (str): A string for which the number of tokens needs to be counted.
        model (str): A string containing the name of the AI model.

    Returns:
        num_tokens (int): An integer representing the number of tokens in the given string.
    """
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

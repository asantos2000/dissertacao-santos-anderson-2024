
import tiktoken

def estimate_tokens(text, model="gpt-4o"):
    """
    Estimates the number of tokens in a given text using the OpenAI `tiktoken` library, 
    which closely approximates the tokenization method used by OpenAI language models.

    Parameters:
        text (str): The text to be tokenized and counted.
        model (str): The model to use for tokenization. Defaults to "gpt-4o".
                     Supported models include "gpt-3.5-turbo" and "gpt-4o".

    Returns:
        int: The estimated number of tokens in the text.
    
    Raises:
        ValueError: If the specified model is not supported by `tiktoken`.

    Example:
        >>> text = "This is a sample text."
        >>> estimate_tokens_tiktoken(text)
        6
    """
    # Load the appropriate tokenizer
    try:
        tokenizer = tiktoken.encoding_for_model(model)
    except KeyError:
        raise ValueError(f"Model '{model}' is not supported by tiktoken.")
    
    # Tokenize the text and return the token count
    tokens = tokenizer.encode(text)
    return len(tokens)

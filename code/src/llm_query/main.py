
import time
from openai import OpenAI
import instructor
import logging
from typing import Any

# Set up basic logging configuration for the checkpoint module
logging.basicConfig(
    level=logging.INFO,  # Set to INFO or another level as needed
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def measure_time(func):
    """
    Decorator to measure the execution time of a function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Execution time for {func.__name__}: {elapsed_time:.2f} seconds")
        return result[0], result[1], elapsed_time
    return wrapper

@measure_time
def query_instruct_llm(system_prompt: str,
                        user_prompt: str,
                        llm_model: str,
                        document_model: Any,
                        temperature: float,
                        max_tokens: int) -> Any:
    """
    Queries the LLM with the given system and user prompts.

    Args:
        system_prompt (str): The system prompt to set the context for the LLM.
        user_prompt (str): The user prompt containing the text to analyze.

    Returns:
        Any: The response from the LLM, parsed into a document_model object.

    Raises:
        Exception: If the API call fails.
    """
    client = instructor.from_openai(OpenAI())
    resp, completion = client.chat.completions.create_with_completion(
        model=llm_model,
        response_model=document_model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    logger.info(f"Tokes used: {completion.usage}")
    return resp, completion

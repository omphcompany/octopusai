from langchain.text_splitter import CharacterTextSplitter

def get_text_chunks(raw_text):
    """
    Generate the function comment for the given function body in a markdown code block with the correct language syntax.

    Args:
        raw_text (str): The raw text to be split into chunks.

    Returns:
        list: A list of text chunks.
    """
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    
    chunks = text_splitter.split_text(raw_text)
    return chunks
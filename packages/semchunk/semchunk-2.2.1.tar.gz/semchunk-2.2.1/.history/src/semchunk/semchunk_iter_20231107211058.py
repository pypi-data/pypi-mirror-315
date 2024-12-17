import re

NON_WHITESPACE_SEMANTIC_SPLITTERS = (
    '.', '?', '!', '*', # Sentence terminators.
    ';', ',', '(', ')', '[', ']', "“", "”", '‘', '’', "'", '"', '`', # Clause separators.
    ':', '—', '…', # Sentence interrupters.
    '/', '\\', '–', '&', '-', # Word joiners.
)
"""A tuple of semantically meaningful non-whitespace splitters that may be used to chunk texts, ordered from most desirable to least desirable."""
    
def _split_text(text: str) -> tuple[str, list[str]]:
    """Split text using the most semantically meaningful splitter possible."""

    # Try splitting at, in order of most desirable to least desirable:
    # - The largest sequence of newlines and/or carriage returns;
    # - The largest sequence of tabs;
    # - The largest sequence of whitespace characters; and
    # - A semantically meaningful non-whitespace splitter.
    if '\n' in text or '\r' in text:
        splitter = max(re.findall(r'[\r\n]+', text))
    
    elif '\t' in text:
        splitter = max(re.findall(r'\t+', text))
    
    elif re.search(r'\s', text):
        splitter = max(re.findall(r'\s+', text))
    
    else:
        # Identify the most desirable semantically meaningful non-whitespace splitter present in the text.
        for splitter in NON_WHITESPACE_SEMANTIC_SPLITTERS:
            if splitter in text:
                break
        
        # If no semantically meaningful splitter is present in the text, return an empty string as the splitter and the text as a list of characters.
        else: # NOTE This code block will only be executed if the for loop completes without breaking.
            return '', list(text)
    
    # Return the splitter and the split text.
    return splitter, text.split(splitter)

def chunk(text: str, chunk_size: int, token_counter: callable) -> list[str]:
    """Split text into semantically meaningful chunks of a specified size as determined by the provided token counter.

   Args:
        text (str): The text to be chunked.
        chunk_size (int): The maximum number of tokens a chunk may contain.
        token_counter (callable): A callable that takes a string and returns the number of tokens in it.
    
    Returns:
        list[str]: A list of chunks up to `chunk_size`-tokens-long, with any whitespace used to split the text removed."""
    
    chunks = []
    queue = [(text, 0)]

    while queue:
        # Pop the first text and index from the queue.
        text, chunk_i = queue.pop()
        
        # Split the text using the most semantically meaningful splitter possible.
        splitter, splits = _split_text(text)
        
        # Initalise a list of indices of splits to skip when iterating through splits because they have already been merged with a previous split into a chunk.
        skips = []
        
        # Iterate through the splits.
        for split_i, split in enumerate(splits):
            # Skip the split if it has already been merged with a previous split into a chunk.
            if split_i in skips:
                continue
            
            # If the split is within the chunk size, add it and all other subsequent splits as a new chunk until the chunk size is reached.
            if token_counter(split) <= chunk_size:
                # Initialise a list of splits to be merged into a new chunk.
                new_chunk_splits = [split]
                
                # Iterate through each subsequent split until the chunk size is reached.
                for next_split_i, next_split in enumerate(splits[split_i+1:], start=split_i+1):
                    # Check whether the next split can be added to the new chunk without exceeding the chunk size.
                    if token_counter(splitter.join(new_chunk_splits+[next_split])) <= chunk_size:
                        # Add the next split to the new chunk.
                        new_chunk_splits.append(next_split)
                        
                        # Add the index of the next split to the list of indices to skip.
                        skips.append(next_split_i)
                    
                    # If the next split cannot be added to the new chunk without exceeding the chunk size, break.
                    else:
                        break
                
                # Merge the splits into a new chunk.
                new_chunk = splitter.join(new_chunk_splits)
                
                # Insert the new chunk and its splitter (or `None` if the splitter is whitespace) into the chunks at the current chunk index.
                chunks.insert(chunk_i, new_chunk)
                
                # Increment the current chunk index by 1.
                chunk_i += 1
                
            # If the split is over the chunk size, add it to the queue.
            else:
                queue.append((split, chunk_i))
    
    # Remove empty chunks.
    for chunk in chunks:
        if not chunk:
            del chunk
    
    return chunks
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
    
    # If the text is already within the chunk size, return it as the only chunk.
    if token_counter(text) <= chunk_size:
        return [text]

    # Split the text using the most semantically meaningful splitter possible.
    splitter, splits = _split_text(text)
    
    # Flag whether the splitter is whitespace.
    splitter_is_whitespace = not splitter.split()
    
    chunks = []
    skips = []
    """A list of indices of splits to skip because they have already been added to a chunk."""
    
    # Iterate through the splits.
    for i, split in enumerate(splits):
        # Skip the split if it has already been added to a chunk.
        if i in skips:
            continue
        
        # Determine whether this is the last split factoring in skips.
        is_last_split = i == len(splits) - 1 or all(j in skips for j in range(i+1, len(splits)))
        
        # If:
        # - This split is over the chunk size, or
        # - The splitter is not whitespace and this is not the last split, and this split plus the splitter is over the chunk size,
        # then recursively chunk the split.
        if (token_counter(split+splitter) if not splitter_is_whitespace and not is_last_split else token_counter(split)) > chunk_size:
            # If the splitter is bringing us over the chunk size (indicated by the split being less than or equal to the chunk size), recursively chunk the split to the chunk size minus the length of the splitter.
            recursive_chunk_size = chunk_size if token_counter(split) > chunk_size else chunk_size-token_counter(splitter)
            new_chunks = chunk(split, recursive_chunk_size, token_counter=token_counter)
            
            # If the splitter is not whitespace, this is not the last split and the last chunk plus the splitter is still over the chunk size, progressively reduce the chunk size until that is not the case or the chunk size is 1.
            while not splitter_is_whitespace and not is_last_split and token_counter(new_chunks[-1]+splitter) > chunk_size and recursive_chunk_size > 1:
                recursive_chunk_size -= 1
                new_chunks = chunk(split, recursive_chunk_size, token_counter=token_counter)

        # If the split is equal to or under the chunk size, merge it with all subsequent splits until the chunk size is reached.
        else:
            # Initialise a list of splits to be merged into a new chunk.
            new_chunk = [split]
            
            # Iterate through each subsequent split until the chunk size is reached.
            for j, next_split in enumerate(splits[i+1:], start=i+1):
                # Check whether the next split can be added to the chunk without exceeding the chunk size.
                if token_counter(splitter.join(new_chunk+[next_split])) <= chunk_size:
                    # Add the next split to the chunk.
                    new_chunk.append(next_split)
                    
                    # Add the index of the next split to the list of indices to skip.
                    skips.append(j)
                
                # If the next split cannot be added to the chunk without exceeding the chunk size, break.
                else:
                    break
            
            # Join the splits with the splitter.
            new_chunk = splitter.join(new_chunk)
            
            # Add the chunk.
            chunks.append(new_chunk)

        # Re-determine whether this is the last split factoring in skips.
        is_last_split = i == len(splits) - 1 or all(j in skips for j in range(i+1, len(splits)))
        
        # If the splitter is not whitespace and the split is not the last split, add the splitter to the end of the last chunk.
        if not splitter_is_whitespace and not is_last_split:
            chunks[-1] += splitter

    return chunks
# New version:
# - Use loop instead of recursion
# - Only add if under chunk size
# - Add splitter to end of last chunk if not whitespace and not last split (right after splitting text).
import re
    
def _split_text(text: str) -> tuple[str, list[str]]:
    """Split text using the most semantically meaningful splitter possible."""

    # Try splitting at, in order of most desirable to least desirable:
    # - The largest sequence of newlines and/or carriage returns;
    # - The largest sequence of tabs; and
    # - The largest sequence of whitespace characters.
    if '\n' in text or '\r' in text:
        splitter = max(re.findall(r'[\r\n]+', text))
    
    elif '\t' in text:
        splitter = max(re.findall(r'\t+', text))
    
    elif re.search(r'\s', text):
        splitter = max(re.findall(r'\s+', text))
    
    # TODO Add notes.
    else:
        return '', list(text)
    
    # TODO Add notes.
    return text.split(splitter)

def chunk(text: str, chunk_size: int, token_counter: callable, _recursion_depth: int = 0) -> list[str]:
    """Split text into semantically meaningful chunks of a specified size as determined by the provided token counter.

   Args:
        text (str): The text to be chunked.
        chunk_size (int): The maximum number of tokens a chunk may contain.
        token_counter (callable): A callable that takes a string and returns the number of tokens in it.
    
    Returns:
        list[str]: A list of chunks up to `chunk_size`-tokens-long, with any whitespace used to split the text removed."""

    # Split the text using the most semantically meaningful splitter possible.
    splitter, splits = _split_text(text)
    
    # TODO
    if splitter.split():
        new_splits = []
        for split in splits[:-1]:
            new_splits.append(split)
            new_splits.append(splitter)
        
        new_splits.extend(splits[-1:])
        splits = new_splits
        
    splits = [split for split in splits if split]
    
    chunks = []
    skips = []
    """A list of indices of splits to skip because they have already been added to a chunk."""
    
    # Iterate through the splits.
    for i, split in enumerate(splits):
        # Skip the split if it has already been added to a chunk.
        if i in skips:
            continue
        
        # If the split is over the chunk size, recursively chunk it.
        if token_counter(split) >= chunk_size:
            chunks.extend(chunk(split, chunk_size, token_counter=token_counter, _recursion_depth=_recursion_depth+1))

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
    
    # If this is not a recursive call, remove any empty chunks.
    if not _recursion_depth:
        chunks = [chunk for chunk in chunks if chunk]
    
    return chunks
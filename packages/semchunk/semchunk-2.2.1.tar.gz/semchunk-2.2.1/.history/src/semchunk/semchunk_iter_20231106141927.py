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
    # If the text is already within the chunk size, return it as the only chunk.
    if token_counter(text) <= chunk_size:
        return [text]
    
    chunks = []
    stack = [(text, 0)]

    while stack:
        # Pop the first text and index from the stack.
        text, chunk_i = stack.pop(0)
        
        # Split the text using the most semantically meaningful splitter possible.
        splitter, splits = _split_text(text)
        
        # If the splitter is not whitespace, create a copy to be reattached to chunks, otherwise use `None` to indicate that no splitter is to be reattached.
        reattach_splitter = splitter if not splitter.split() else None
        
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
                
                # Add the new chunk and its splitter to the chunks.
                chunks.append((new_chunk, splitter))
            
            
            

        if token_counter(text) <= chunk_size:
            chunks.append(text)
        else:
            splitter, splits = _split_text(text)
            splitter_is_whitespace = not splitter.split()
            skips = []

            for i, split in enumerate(splits):
                if i in skips:
                    continue

                if token_counter(split) > chunk_size:
                    stack.append(split)
                else:
                    new_chunk_splits = [split]
                    for j, next_split in enumerate(splits[i+1:], start=i+1):
                        if token_counter(splitter.join(new_chunk_splits+[next_split])) <= chunk_size:
                            new_chunk_splits.append(next_split)
                            skips.append(j)
                        else:
                            break

                    new_chunk_splits = splitter.join(new_chunk_splits)
                    chunks.append(new_chunk_splits)

                if not splitter_is_whitespace and not (i == len(splits) - 1 or all(j in skips for j in range(i+1, len(splits)))):
                    if token_counter(chunks[-1]+splitter) <= chunk_size:
                        chunks[-1] += splitter
                    else:
                        chunks.append(splitter)

    chunks = [chunk for chunk in chunks if chunk]
    return chunks





    splitters = ('\n\n\n', '\n\n') + NON_WHITESPACE_SEMANTIC_SPLITTERS
    chunks = []
    stack = [text]
    
    while stack:
    
    for splitter in splitters:
        if splitter not in text:
            continue
        
        splits = text.split(splitter)
        skips = []
        
        for i, split in enumerate(splits):
            if token_counter(split) <= chunk_size:
                new_chunk_splits = [split]
            
                # Iterate through each subsequent split until the chunk size is reached.
                for j, next_split in enumerate(splits[i+1:], start=i+1):
                    # Check whether the next split can be added to the chunk without exceeding the chunk size.
                    if token_counter(splitter.join(new_chunk_splits+[next_split])) <= chunk_size:
                        # Add the next split to the chunk.
                        new_chunk_splits.append(next_split)
                        
                        # Add the index of the next split to the list of indices to skip.
                        skips.append(j)
                    
                    # If the next split cannot be added to the chunk without exceeding the chunk size, break.
                    else:
                        break
            
            else:
                
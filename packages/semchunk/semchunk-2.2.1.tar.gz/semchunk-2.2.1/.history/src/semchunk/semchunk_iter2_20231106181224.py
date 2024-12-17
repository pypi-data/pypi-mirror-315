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
    queue = [(text, 0, None)]

    while queue:
        # Pop the first text and index from the queue.
        text, first_chunk_i, parent_splitter = queue.pop(0)
        
        # Set the current chunk index to the first chunk index.
        current_chunk_i = first_chunk_i
        
        # Split the text using the most semantically meaningful splitter possible.
        splitter, splits = _split_text(text)
        
        # If the splitter is not whitespace, create a copy to be reattached to chunks otherwise use `None` to indicate that no splitter should be reattached.
        reattach_splitter = splitter if splitter.split() else None
        
        # Initalise a list of indices of splits to skip when iterating through splits because they have already been merged with a previous split into a chunk.
        skips = []
        print('Text:', text, 'Splitter:', splitter, 'Parent Splitter:', parent_splitter, 'Chunks:', chunks, 'Index:', current_chunk_i)
        
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
                chunks.insert(current_chunk_i, (new_chunk, reattach_splitter))
                
                # Increment the current chunk index by 1.
                current_chunk_i += 1
                
            # If the split is over the chunk size, add it to the queue.
            else:
                queue.append((split, current_chunk_i, reattach_splitter))
    
    # TODO FIXME BUG '.' not getting added where it should be.
    
    # Reattach splitters to chunked texts, remove splitters from chunks and filter out empty chunks.
    i = -1
    
    while i < len(chunks)-1:
        i += 1
        
        # Remove empty chunks.
        if not chunks[i][0]:
            del chunks[i]
            i -= 1
            continue

        # Remove the splitter from the chunk.
        chunks[i] = chunks[i][0]
        
        # If there is a next chunk and the next chunk has a splitter to reattach, reattach the splitter of the next chunk to the end of the current chunk if doing so would not cause the current chunk to exceed the chunk size otherwise add the splitter as a new chunk and remove it from the next chunk.
        if i < len(chunks)-1 and chunks[i+1][1]:
            splitter = chunks[i+1][1]
            
            if token_counter(chunks[i] + splitter) <= chunk_size:
                chunks[i] += splitter
            
            else:
                chunks[i+1] = chunks[i+1][0], None
                chunks.insert(i+1, splitter)

    #print(chunks)
    return chunks
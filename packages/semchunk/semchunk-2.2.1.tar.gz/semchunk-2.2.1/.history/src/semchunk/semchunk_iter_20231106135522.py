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
    splitters = ('\n\n\n', '\n\n') + NON_WHITESPACE_SEMANTIC_SPLITTERS
    chunks = []
    
    for splitter in splitters:
        if splitter not in text:
            continue
        
        splits = text.split(splitter)
        skips = []
        
        for i, split in enumerate(splits):
            if token_counter(split) <= chunk_size:
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
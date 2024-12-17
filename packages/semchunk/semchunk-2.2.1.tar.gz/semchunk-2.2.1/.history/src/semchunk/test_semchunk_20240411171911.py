import re

from typing import Callable
from functools import cache, wraps

_memoised_token_counters = {}
"""A map of token counters to their memoised versions."""

_NON_WHITESPACE_SEMANTIC_SPLITTERS = (
    '.', '?', '!', '*', # Sentence terminators.
    ';', ',', '(', ')', '[', ']', "“", "”", '‘', '’', "'", '"', '`', # Clause separators.
    ':', '—', '…', # Sentence interrupters.
    '/', '\\', '–', '&', '-', # Word joiners.
)
"""A tuple of semantically meaningful non-whitespace splitters that may be used to chunk texts, ordered from most desirable to least desirable."""

def _split_text(text: str) -> tuple[str, bool, list[str]]:
    """Split text using the most semantically meaningful splitter possible."""
    
    splitter_is_whitespace = True

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
        for splitter in _NON_WHITESPACE_SEMANTIC_SPLITTERS:
            if splitter in text:
                splitter_is_whitespace = False
                break
        
        # If no semantically meaningful splitter is present in the text, return an empty string as the splitter and the text as a list of characters.
        else: # NOTE This code block will only be executed if the for loop completes without breaking.
            return '', splitter_is_whitespace, list(text)
    
    # Return the splitter and the split text.
    return splitter, splitter_is_whitespace, text.split(splitter)

def chunk(text: str, chunk_size: int, token_counter: Callable, memoize: bool=True, _recursion_depth: int = 0) -> list[str]:
    """Split text into semantically meaningful chunks of a specified size as determined by the provided token counter.

   Args:
        text (str): The text to be chunked.
        chunk_size (int): The maximum number of tokens a chunk may contain.
        token_counter (callable): A callable that takes a string and returns the number of tokens in it.
        memoize (bool, optional): Whether to memoise the token counter. Defaults to True.
    
    Returns:
        list[str]: A list of chunks up to `chunk_size`-tokens-long, with any whitespace used to split the text removed."""
    
    # If this is not a recursive call and memoization is enabled, overwrite the `token_counter` with a memoised version of itself.
    if not _recursion_depth and memoize:
        token_counter = _memoised_token_counters.setdefault(token_counter, cache(token_counter))

    # Split the text using the most semantically meaningful splitter possible.
    splitter, splitter_is_whitespace, splits = _split_text(text)
    
    chunks = []
    skips = set()
    """A list of indices of splits to skip because they have already been added to a chunk."""
    
    # Iterate through the splits.
    for i, split in enumerate(splits):
        # Skip the split if it has already been added to a chunk.
        if i in skips:
            continue
        
        # If the split is over the chunk size, recursively chunk it.
        if token_counter(split) > chunk_size:
            chunks.extend(chunk(split, chunk_size, token_counter, memoize, _recursion_depth+1))

        # If the split is equal to or under the chunk size, merge it with all subsequent splits until the chunk size is reached.
        else:
            # Binary search for the maximum number of splits that may be merged without exceeding the chunk size.
            mergables = splits[i:]
            minimum_possible_merges = 0
            maximum_possible_merges = len(mergables) + 1
            
            while minimum_possible_merges < maximum_possible_merges:
                # Test whether merging at the midpoint of the known minimum and maximum possible merges floor divided by 8 (in order to bias the search towards shorter sequences as it is much more expensive to count longer sequences) would exceed the chunk size and if it would, update the maximum number of possible merges accordingly, otherwise update the minimum number of possible merges.
                merge_index = minimum_possible_merges + (maximum_possible_merges - minimum_possible_merges) // 8
                merged = splitter.join(mergables[:merge_index])
                
                if token_counter(merged) > chunk_size:
                    maximum_possible_merges = merge_index
                
                else:
                    minimum_possible_merges = merge_index + 1
            
            # Store the merged chunk.
            merge_index = minimum_possible_merges - 1
            merged = splitter.join(mergables[:merge_index])
            
            chunks.append(merged)
            
            # Add the indices of any splits we have merged to the list of indices to skip.
            skips.update(range(i + 1, i + merge_index))

        # If the splitter is not whitespace and the split is not the last split, add the splitter to the end of the last chunk if doing so would not cause it to exceed the chunk size otherwise add the splitter as a new chunk.
        if not splitter_is_whitespace and not (i == len(splits) - 1 or all(j in skips for j in range(i+1, len(splits)))):
            # We seperately add tokens(prior chunk) and tokens(splitter) to ensure O(1) - (both will be in cache).
            # There is a failure case where tokens(get_last_token(prior_chunk) + splitter) == 1 however this is
            # quite uncommon and leads to a negligible impact
            if token_counter(chunks[-1]) + token_counter(splitter) <= chunk_size:
                chunks[-1] += splitter
            else:
                chunks.append(splitter)
    
    # If this is not a recursive call, remove any empty chunks.
    if not _recursion_depth:
        chunks = list(filter(None, chunks))
    
    return chunks

chunk = wraps(chunk)(cache(chunk))
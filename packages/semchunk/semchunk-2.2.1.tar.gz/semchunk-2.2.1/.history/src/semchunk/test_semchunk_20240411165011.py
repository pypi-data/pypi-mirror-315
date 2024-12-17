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

def chunk_legacy(text: str, chunk_size: int, token_counter: Callable, memoize: bool=True, _recursion_depth: int = 0) -> list[str]:
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
            chunks.extend(chunk_legacy(split, chunk_size, token_counter=token_counter, memoize=memoize, _recursion_depth=_recursion_depth+1))

        # If the split is equal to or under the chunk size, merge it with all subsequent splits until the chunk size is reached.
        else:
            # Initalise the new chunk.
            new_chunk = split
            
            # Iterate through each subsequent split until the chunk size is reached.
            for j, next_split in enumerate(splits[i+1:], start=i+1):
                # Check whether the next split can be added to the chunk without exceeding the chunk size.
                if token_counter(updated_chunk:=new_chunk+splitter+next_split) <= chunk_size:
                    # Add the next split to the new chunk.
                    new_chunk = updated_chunk
                    
                    # Add the index of the next split to the list of indices to skip.
                    skips.add(j)
                
                # If the next split cannot be added to the chunk without exceeding the chunk size, break.
                else:
                    break
            
            # Add the chunk.
            chunks.append(new_chunk)

        # If the splitter is not whitespace and the split is not the last split, add the splitter to the end of the last chunk if doing so would not cause it to exceed the chunk size otherwise add the splitter as a new chunk.
        if not splitter_is_whitespace and not (i == len(splits) - 1 or all(j in skips for j in range(i+1, len(splits)))):
            if token_counter(last_chunk_with_splitter:=chunks[-1]+splitter) <= chunk_size:
                chunks[-1] = last_chunk_with_splitter
            
            else:
                chunks.append(splitter)
    
    # If this is not a recursive call, remove any empty chunks.
    if not _recursion_depth:
        chunks = list(filter(None, chunks))
    
    return chunks

def count(text: str, max_size: int, counter: Callable) -> int:
    """Counts the number of tokens in a text, with a heuristic to accelerate long texts"""
    heuritistic = 6*max_size

    # There is a rare failure case for the below heuristic where superfluous tokens 
    # may be added from a longer, existing token being split before it was finished.
    # e.g. Australia -> 1 token
    #      Australi  -> 3 token
    #
    # We mitigate this failure case by adding the len(longest token)-1 such that
    # any ongoing token will be able to finish
    #
    # Using the cl100k tokenset, the length of the longest non-symbol token is 42
    # See: https://gist.github.com/Yardanico/623b3092d0b707119f8c7d90a3596afe
    max_token = 42 - 1

    if len(text) > heuritistic and counter(text[:heuritistic+max_token]) > max_size:
        return max_size+1
    return counter(text)

# def _merge_chunks(chunks: list[str], chunk_size: int, splitter: str, token_counter: Callable) -> tuple[str, int]:
#     """Merge chunks until the chunk size is reached."""
    
#     # Binary search for the maximum number of chunks that may be merged without exceeding the chunk size.
#     minimum_possible_merges = 0
#     maximum_possible_merges = len(chunks) + 1
    
#     while minimum_possible_merges < maximum_possible_merges:
#         # Test whether merging at the midpoint of the known minimum and maximum possible merges floor divided by 8 (in order to bias the search towards shorter sequences as it is much more expensive to count longer sequences) would exceed the chunk size and if it would, update the maximum number of possible merges accordingly, otherwise update the minimum number of possible merges.
#         merged_chunks = splitter.join(chunks[:test_merge:=minimum_possible_merges + (maximum_possible_merges - minimum_possible_merges) // 8])
        
#         if token_counter(merged_chunks) > chunk_size:
#             maximum_possible_merges = test_merge
        
#         else:
#             minimum_possible_merges = test_merge + 1
    
#     # Return the merged chunks along with the index of the last mergable chunk.
#     return merged_chunks

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
        if count(split, chunk_size, token_counter) > chunk_size:
            chunks.extend(chunk(split, chunk_size, token_counter, memoize, _recursion_depth+1))

        # If the split is equal to or under the chunk size, merge it with all subsequent splits until the chunk size is reached.
        else:
            # Binary search for the maximum number of splits that may be merged without exceeding the chunk size.
            mergables = splits[i:]
            minimum_possible_merges = 0
            maximum_possible_merges = len(mergables) + 1
            
            while minimum_possible_merges < maximum_possible_merges:
                # Test whether merging at the midpoint of the known minimum and maximum possible merges floor divided by 8 (in order to bias the search towards shorter sequences as it is much more expensive to count longer sequences) would exceed the chunk size and if it would, update the maximum number of possible merges accordingly, otherwise update the minimum number of possible merges.
                merged = splitter.join(mergables[:(merge_index:=minimum_possible_merges + (maximum_possible_merges - minimum_possible_merges) // 8)])
                
                if token_counter(merged) > chunk_size:
                    maximum_possible_merges = merge_index
                
                else:
                    minimum_possible_merges = merge_index + 1
            
            # Store the merged chunk.
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
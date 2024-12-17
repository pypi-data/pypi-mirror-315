"""Test semchunk."""
import semchunk

import nltk
import tiktoken
import transformers

# Download the Gutenberg corpus.
nltk.download('gutenberg')
gutenberg = nltk.corpus.gutenberg

# Initalise the encoder.
encoder = tiktoken.encoding_for_model('gpt-4')

def _token_counter(text: str) -> int:
    """Count the number of tokens in a text."""
    
    return len(encoder.encode(text))

def test_chunk() -> None:
    """Test `semchunk.chunk()`."""
    
    # Test a variety of chunk sizes.
    for chunk_size in {1, 2, 512}:
        # Test a variety of texts.
        for fileid in {'austen-emma.txt', 'carroll-alice.txt', 'shakespeare-macbeth.txt'}:
            sample = gutenberg.raw(fileid)
            
            chunker = semchunk.make_chunker(encoder, chunk_size)
            
            for chunk in chunker(sample):
                assert _token_counter(chunk) <= chunk_size
            
            # Test that recombining lowercased chunks stripped of whitespace yields the original text.
            lowercased_no_whitespace = ''.join(sample.lower().split())
            assert ''.join(chunker(lowercased_no_whitespace, token_counter = _token_counter)) == lowercased_no_whitespace
    
    # Test a string where tabs must be used as splitters (to increase code coverage).
    chunker = semchunk.make_chunker(_token_counter, 4)
    assert chunker('ThisIs\tATest.', 4) == ['ThisIs', 'ATest.']
    
    # Test using semchunk directly with memoization enabled.
    assert semchunk.chunk('ThisIs\tATest.', 4, _token_counter, memoize = True) == ['ThisIs', 'ATest.']
    
    # Test chunking multiple texts.
    chunker = semchunk.make_chunker(_token_counter, 4)
    assert chunker(['ThisIs\tATest.', 'ThisIs\tATest.'], 4) == [['ThisIs', 'ATest.'], ['ThisIs', 'ATest.']]
    
    # 
"""Test semchunk."""
import semchunk

import nltk
import tiktoken
import transformers

def test_chunk() -> None:
    """Test `semchunk.chunk()`."""
    
    # Download the Gutenberg corpus.
    nltk.download('gutenberg')
    gutenberg = nltk.corpus.gutenberg
    
    # Initalise the tokenizers.
    tiktoken_tokenizer = tiktoken.encoding_for_model('gpt-4')

    def tiktoken_token_counter(text: str) -> int:
        """Count the number of tokens in a text."""
        
        return len(tiktoken_tokenizer.encode(text))
    
    transformers_tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2')
    
    # Test chunking with a variety of chunk sizes.
    for chunk_size in {1, 2, 512}:
        # Test chunking with a variety of texts.
        for fileid in {'austen-emma.txt', 'carroll-alice.txt', 'shakespeare-macbeth.txt'}:
            sample = gutenberg.raw(fileid)
            
            chunker = semchunk.make_chunker(tiktoken_tokenizer, chunk_size)
            
            for chunk in chunker(sample):
                assert tiktoken_token_counter(chunk) <= chunk_size
            
            # Verify that recombining lowercased chunks stripped of whitespace yields the original text.
            lowercased_no_whitespace = ''.join(sample.lower().split())
            assert ''.join(chunker(lowercased_no_whitespace, token_counter = tiktoken_token_counter)) == lowercased_no_whitespace
    
    # Test a string where tabs must be used as splitters.
    chunker = semchunk.make_chunker(tiktoken_token_counter, 4)
    assert chunker('ThisIs\tATest.', 4) == ['ThisIs', 'ATest.']
    
    # Test using semchunk directly with memoization enabled.
    assert semchunk.chunk('ThisIs\tATest.', 4, tiktoken_token_counter, memoize = True) == ['ThisIs', 'ATest.']
    
    # Test chunking multiple texts.
    chunker = semchunk.make_chunker(tiktoken_token_counter, 4)
    assert chunker(['ThisIs\tATest.', 'ThisIs\tATest.'], 4) == [['ThisIs', 'ATest.'], ['ThisIs', 'ATest.']]
    
    # Test using a `transformers` tokenizer.
    tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2')
    assert semchunk.chunk('This is a test.', 1, lambda text: len(tokenizer.encode(text))) == ['This', 'is', 'a', 'test.']
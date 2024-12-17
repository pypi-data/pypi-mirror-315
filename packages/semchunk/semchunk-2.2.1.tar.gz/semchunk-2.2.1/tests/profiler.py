"""Test semchunk."""
import time
import sys
sys.path.append('D:/workspace/semchunk/')
import src.semchunk.semchunk as semchunk
import tiktoken
import nltk

nltk.download('gutenberg')
encoder = tiktoken.encoding_for_model('gpt-4')
gutenberg = nltk.corpus.gutenberg

def _token_counter(text: str) -> int:
    return len(encoder.encode(text))

def test_chunk(chunk_sizes, fileids):
    for chunk_size in chunk_sizes:
        for fileid in fileids:
            print(f'Testing {fileid} with chunk size {chunk_size}.')
            
            sample = gutenberg.raw(fileid)
            for chunk in semchunk.chunk(sample, chunk_size=chunk_size, token_counter=_token_counter):
                assert _token_counter(chunk) <= chunk_size
            
            # Test that recombining lowercased chunks stripped of whitespace yields the original text.
            lowercased_no_whitespace = ''.join(sample.lower().split())
            assert ''.join(semchunk.chunk(lowercased_no_whitespace, chunk_size, _token_counter)) == lowercased_no_whitespace

chunk_sizes = {512, 1024, 2048}
fileids = gutenberg.fileids()

start = time.time()
test_chunk(chunk_sizes, fileids)
end = time.time()
print('Took', end-start, 'seconds')
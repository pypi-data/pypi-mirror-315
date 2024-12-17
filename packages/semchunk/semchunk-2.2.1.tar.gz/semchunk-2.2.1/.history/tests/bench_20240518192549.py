import semchunk
from semantic_text_splitter import TextSplitter
import test_semchunk
import time

chunk_size = 512
semantic_text_splitter_chunker = TextSplitter.from_tiktoken_model('gpt-4', chunk_size)

def bench_semchunk(text: str) -> None:
    semchunk.chunk(text, chunk_size=chunk_size, token_counter=test_semchunk.tiktoken_token_counter)

def bench_semantic_text_splitter(text: str) -> None:
    semantic_text_splitter_chunker.chunks(text)

libraries = {
    'semchunk': bench_semchunk,
    'semantic_text_splitter': bench_semantic_text_splitter,
}

def bench() -> dict[str, float]:
    benchmarks = dict.fromkeys(libraries.keys(), 0)
    
    for fileid in test_semchunk.gutenberg.fileids():
        sample = test_semchunk.gutenberg.raw(fileid)
        for library, function in libraries.items():
            start = time.time()
            function(sample)
            benchmarks[library] += time.time() - start
    
    return benchmarks

if __name__ == '__main__':
    for library, time_taken in bench().items():
        print(f'{library}: {time_taken:.2f}s')
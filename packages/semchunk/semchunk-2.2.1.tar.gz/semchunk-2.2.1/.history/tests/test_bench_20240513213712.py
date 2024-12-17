import semchunk as older_semchunk
import sys
sys.path.append('D:/workspace/semchunk/')
import src.semchunk.semchunk as newer_semchunk
# import src.semchunk.dev_semchunk as dev_semchunk
import semantic_text_splitter
import test_semchunk
import time
import tiktoken

chunk_size = 512
semantic_text_splitter_chunker = TextSplitter.from_tiktoken_model('gpt-4', chunk_size)
encoder = tiktoken.encoding_for_model('gpt-4')

def bench_older_semchunk(text: str) -> None:
    older_semchunk.chunk(text, chunk_size=chunk_size, token_counter=test_semchunk._token_counter)

def bench_newer_semchunk(text: str) -> None:
    newer_semchunk.chunk(text, chunk_size=chunk_size, token_counter=test_semchunk._token_counter)

# def bench_dev_semchunk(text: str) -> None:
#     dev_semchunk.chunk(text, chunk_size=chunk_size, token_counter=test_semchunk._token_counter)

def bench_semantic_text_splitter(text: str) -> None:
    semantic_text_splitter_chunker.chunks(text)

libraries = {
    'older_semchunk': bench_older_semchunk,
    'newer_semchunk': bench_newer_semchunk,
    # 'dev_semchunk': bench_dev_semchunk,
    #'semantic_text_splitter': bench_semantic_text_splitter,
}

def bench() -> dict[str, float]:
    benchmarks: dict[str, float] = dict.fromkeys(libraries.keys(), 0.0)
    
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
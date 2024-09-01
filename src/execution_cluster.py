from flask import Flask, request, jsonify
import numpy as np
import multiprocessing as mp
from heapq import merge
from functools import wraps
from time import time

app = Flask(__name__)

# decorator, i.e. f: function_i -> function_j
def measure_exec_time(f):
    @wraps(f)
    def wrap(*args, **kw):
        t_start = time()
        result = f(*args, **kw)
        t_end = time()
        exec_time = t_end - t_start
        print(f'func: {f.__name__} took: {exec_time:.4f} sec')
        return ( result, exec_time )
    return wrap

def sort_chunk(vector: list[int]) -> list[int]:
    return sorted(vector)

@measure_exec_time
def sequential_sort(vector: list[int]) -> list[int]:
    return sorted(vector)

@measure_exec_time
def parallel_sort(vector: list[int], num_threads: int) -> list[int]:
    num_threads = min(num_threads, len(vector))
    chunk_size = (len(vector) + num_threads - 1) // num_threads
    chunks = [vector[i:i + chunk_size] for i in range(0, len(vector), chunk_size)]

    with mp.Pool(processes=num_threads) as pool:
        sorted_chunks = pool.map(sort_chunk, chunks)
    sorted_vector = list(merge(*sorted_chunks))
    return sorted_vector

# Route to handle the sorting request
@app.route('/sort', methods=['POST'])
def sort_vector() -> None:
    # Parse the JSON payload
    data = request.json
    method = data.get("method")
    seed = data.get("seed")
    size = data.get("size")
    n_repetitions = data.get("n_repetitions")
    n_threads = data.get("n_threads")
    
    # throw away invalid input
    if not method or method not in {"SEC", "PAR"}:
        return jsonify({"error": "Invalid method"}), 400
    if not (
        isinstance(seed, int) and 
        isinstance(size, int) and 
        isinstance(n_repetitions, int) and 
        isinstance(n_threads, int)
    ):
        return jsonify({"error": "Invalid input parameters"}), 400
    
    total_time = 0.0
    np.random.seed(seed)
    for _ in range(n_repetitions):
        vector = np.random.randint(0, size, size=size).tolist()
        if method == "SEC":
            _, exec_time = sequential_sort(vector)
        if method == "PAR":
            _, exec_time = parallel_sort(vector, n_threads)
        total_time += exec_time
    
    average_time = total_time / n_repetitions
    return jsonify({"result": average_time})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

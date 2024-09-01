from flask import Flask, request, jsonify, render_template
import numpy as np
import multiprocessing as mp
from heapq import merge
from functools import wraps
from time import time

app = Flask(__name__)

def measure_exec_time(f):
    @wraps(f)
    def wrap(*args, **kw):
        t_start = time()
        result = f(*args, **kw)
        t_end = time()
        exec_time = t_end - t_start
        print(f'func: {f.__name__} took: {exec_time:.4f} sec')
        return result, exec_time
    return wrap

def sort_chunk(vector):
    return sorted(vector)

@measure_exec_time
def sequential_sort(vector):
    return sorted(vector)

@measure_exec_time
def parallel_sort(vector, num_threads):
    num_threads = min(num_threads, len(vector))
    chunk_size = (len(vector) + num_threads - 1) // num_threads
    chunks = [vector[i:i + chunk_size] for i in range(0, len(vector), chunk_size)]
    with mp.Pool(processes=num_threads) as pool:
        sorted_chunks = pool.map(sort_chunk, chunks)
    return list(merge(*sorted_chunks))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        params = parse_request(request.form)
        vectors = generate_vectors(params['seed'], params['size'], params['n_repetitions'])
        average_time = execute_sorting(vectors, params['method'], params['n_threads'])
        return render_template('index.html', result=average_time)
    return render_template('index.html', result=None)

def parse_request(form_data):
    return {
        'method': form_data.get("method"),
        'seed': int(form_data.get("seed")),
        'size': int(form_data.get("size")),
        'n_repetitions': int(form_data.get("n_repetitions")),
        'n_threads': int(form_data.get("n_threads"))
    }

def generate_vectors(seed, size, n_repetitions):
    np.random.seed(seed)
    return [np.random.randint(0, size, size=size).tolist() for _ in range(n_repetitions)]

def execute_sorting(vectors, method, n_threads):
    total_time = 0.0
    for vector in vectors:
        if method == "SEC":
            _, exec_time = sequential_sort(vector)
        else:
            _, exec_time = parallel_sort(vector, n_threads)
        total_time += exec_time
    return round(total_time / len(vectors), 8)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
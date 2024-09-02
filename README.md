# Flask-WebApp

![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white)
[![Docker](https://img.shields.io/badge/Docker-0db7ed?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python 3.12](https://img.shields.io/badge/Python_3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3120/)

## Overview

This project contains a Flask-based GUI web service designed to perform sorting on randomly generated vectors using either sequential or parallel methods.


<div style="text-align: center;">
    <img src="img/flask_result.png" alt="resulting flask web app" width="400"/>
</div>

## Features

- **Sequential and Parallel Sorting**: Choose between sequential and parallel sorting methods (implemented using the `multiprocessing` module).
- **Execution Time Measurement**: The service measures and returns the average execution time for sorting operations.
- **Customizable Parameters**: Specify the random seed, vector size, number of repetitions, and number of threads for parallel processing.
- **Web Interface**: Render and use a modern-looking web interface to set computational parameters and then to display the result.

## Programming techniques

- Easily **deployable via Docker**
- Use of **decorators** for **benchmarking**
- **Paralelized computation** (classic thread pool) via the `multiprocessing` module
- Use of **numpy** and **seeded random number generator** for generating inputs
- App bult via **Flask** library and contains an interactive web **GUI interface**
- Automatic code **linting** with Github **CI workflow**
- IMHO, just 70 lines of code (`src/iface_cluster.py`) beatifuly showcase the **powerful and concise expressibility** of Python

## Installation

### Prerequisites

- Docker
- Python 3.x (for local development)
- Flask

### Download and Build

You can clone the repository and build the Docker image:

```bash
git git@github.com:nierja/Flask-WebApp.git
cd Flask-WebApp
docker build -t execution-cluster .
```

### Running the Docker Container

To run the container and start the service:

```bash
docker run -p 5000:5000 execution-cluster
```

## Installation and run

After you run either the Docker container or `src/iface_cluster.py` itself, the program displays the localhost addres where you can find the running app.

```python
$ Flask-WebApp git:(main) python src/iface_cluster.py
 * Serving Flask app 'iface_cluster'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.24.211.30:5000
Press CTRL+C to quit
```
# Biological Computation Exercise #2

This repository contains:

- **q1.py**: Main script implementing Q1. Generate motifs of a given size, and optionally outputs them to a file.
- **q2.py**: Main script implementing Q2. Count occurrences of motifs of a given size in an input graph.
- **common.py**: Helper module defining `MotifList` and `generate_motifs`, which are used in both `q1.py` and `q2.py`.
- **requirements.txt**: List of Python package dependencies.
- **.python-version, pyproject.toml, uv.lock**: Optional files if you work with [uv](https://docs.astral.sh/uv/).
- **hw2.ipynb**: A Jupyter notebook used to compose my assignment file uploaded to Moodle. 
- **q2_input_graph_example_1.txt, q2_input_graph_example_2.txt**: Input graphs files for Q2.
- **README.md**: This file.

## Prerequisites

- **Python 3.11+**  
- **pip**
- **uv** (Optional, but would make your life much better & faster). If you decide to use it, replace `python q{num}.py` with `uv run q{num}.py` in the different sections.

### Installation
1.	Clone the repository:
    ```bash
    git clone https://github.com/abuchnick/biological-computation-hw.git
    cd biological-computation-hw/hw2
    ```
2.	(Optional but recommended) Initialize & activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    Or with uv:
    ```bash
    uv venv
    ```
3.	Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
    Or with uv:
    ```bash
    uv sync
    ```

## Usage

### Q1

Generally speaking, you can run this to invoke Q1 script:
```bash
python q1.py --n <motif_size> --output-motifs <file/console>
``` 
For example, in order to generate motifs for n=1..4, run:
```bash
python q1.py --n 1 2 3 4 --output-motifs file
```
For each n in {1, 2, 3, 4}, generates all motifs of size n, and writes the results to motifs_{n}.txt.


### Q2

Generally speaking, you can run this to invoke Q2 script:
```bash
python q2.py --n <motif_size> --input-graph-file <path> --output-subgraphs <file/console>
```
Specifically, for the example provided in the assigment:
```bash
python q2.py --n 4 --input-graph-file q2_input_graph_example.txt --output-subgraphs console
``` 

## AI Usage Disclaimer
Some of the code was generated using AI, specifically by using Cursor IDE.

import argparse
from itertools import combinations
from pathlib import Path
from typing import List

import networkx as nx
from common import MotifList, generate_motifs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n", type=int, required=True, help="Size of motifs (number of nodes)"
    )
    parser.add_argument(
        "--input-graph-file",
        type=Path,
        required=True,
        help="Path to an input graph file.",
    )
    parser.add_argument(
        "--output-subgraphs",
        choices=["file", "console"],
        required=False,
        help="Output mode. If passed, the subgraphs will be written to a file or printed to the console.",
    )
    return parser.parse_args()


def read_graph(graph_file_path: str) -> nx.DiGraph:
    """
    Parses graph from a text file that contains edges in the following format:
    v1 v2
    v3 v4
    ...
    And converts it into a networkx DiGraph.
    Args:
        graph_file_path: The path to the input graph file
    Returns:
        A networkx DiGraph
    """
    print(f"Reading graph from {graph_file_path}...")
    with open(graph_file_path, "r") as f:
        textual_edges = f.readlines()
    edges = []
    for textual_edge in textual_edges:
        u, v = map(int, textual_edge.strip().split())
        edges.append((u, v))
    return nx.DiGraph(edges)


def prepare_textual_output(motif_counts: List[int], motifs: MotifList) -> str:
    """
    Prepare the textual output for the given list of motifs, according to the format specified in the assignment.
    Args:
        motif_counts: A list of counts of motifs
        motifs: A list of motifs to be written to the output channel (file/console).
    Returns:
        A string containing the textual output.
    """
    output = ""
    for i, (count, motif) in enumerate(zip(motif_counts, motifs), start=1):
        output += f"#{i}\n{count=}\n"
        output += f"{motif.edges()}\n"
    return output


def main():
    args = parse_args()

    # Create NetworkX graph from input file
    full_graph = read_graph(args.input_graph_file)

    # Generate all possible node subsets of size n out of the input graph
    available_nodes = list(full_graph.nodes())
    nodes_subsets = list(combinations(available_nodes, args.n))

    # Generate all possible motifs of size n
    motifs = generate_motifs(args.n)
    motif_counts = [0] * len(motifs)

    for nodes_subset in nodes_subsets:
        nodes_subset_set = set(nodes_subset)
        subset_edges = []
        for u, v in full_graph.edges():
            if u in nodes_subset_set and v in nodes_subset_set:
                subset_edges.append((u, v))
        for num_edges in range(len(subset_edges) + 1):
            for edge_combination in combinations(subset_edges, num_edges):
                candidate_graph = nx.DiGraph()
                candidate_graph.add_nodes_from(nodes_subset_set)
                candidate_graph.add_edges_from(edge_combination)
                if not nx.is_weakly_connected(candidate_graph):
                    continue
                for i, motif in enumerate(motifs):
                    if nx.is_isomorphic(motif, candidate_graph):
                        motif_counts[i] += 1
    if not args.output_subgraphs:
        return
    textual_output = prepare_textual_output(motif_counts, motifs)
    if args.output_subgraphs == "file":
        with open("q2.txt", "w") as f:
            f.write(textual_output)
    elif args.output_subgraphs == "console":
        print(textual_output)


if __name__ == "__main__":
    main()

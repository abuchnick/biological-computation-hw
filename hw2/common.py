import time
from collections import defaultdict
from itertools import combinations, permutations
from typing import Dict, List, Tuple

import networkx as nx
import networkx.classes.reportviews as nx_reportviews

MotifList = List[nx.DiGraph]


def generate_motifs(motif_size: int) -> MotifList:
    """
    Generate all possible motifs of a given size.
    Handles trivial cases (N=0, N=1) by returning the empty graph and a single node with a self-loop, respectively.
    For the general case:
    - Generate all possible edges
    - Iterate over all combinations of k possible edges, where k ranges from `motif_size`-1 to the total number of edges
    - For each combination, create a candidate graph and check if it is isomorphic to any of the previously generated graphs.
    - If it is not isomorphic, add it to the list of motifs.
    Note: For optimization purposes, we pre-filter the candidate graphs with invariants before performing the isomorphism test.
    In order to do this, we store the sorted in/out degrees of the nodes and the number of edges of each generated graph in a map, and only perform the isomorphism test if the sorted in/out degrees and the number of edges match.
    Args:
        motif_size: Size of the motif to generate
    Returns:
        A list of all possible motifs of size `motif_size`
    """
    # Handle N=0 case: an empty graph is trivially connected
    if motif_size == 0:
        return [nx.DiGraph()]

    # Generate nodes
    nodes = list(range(1, motif_size + 1))

    # Handle N=1 case: a single node with a self-loop is trivially connected
    if len(nodes) == 1:
        G = nx.DiGraph()
        G.add_node(nodes[0])
        G.add_edge(nodes[0], nodes[0])
        return [G]

    # Generate all possible edges
    possible_edges = list(permutations(nodes, 2))
    print(f"Possible edges count: {len(possible_edges)}")

    # Optimization Data Stores
    motifs_count = 0
    # Map from motif id to (graph_object, sorted_in_degrees, sorted_out_degrees)
    id_to_motif_map: Dict[
        int,
        Tuple[
            nx.DiGraph,
            Tuple[nx_reportviews.InDegreeView],
            Tuple[nx_reportviews.OutDegreeView],
        ],
    ] = dict()
    # Map from number of edges to list of motif ids
    num_edges_to_motif_ids_map: Dict[int, List[int]] = defaultdict(list)

    last_print_time = time.time()

    # Minimum number of edges for a weakly connected graph of size N > 1 is N-1
    min_k = (motif_size - 1) if motif_size > 1 else 1

    # Optimization #1: Only consider combinations of edges that are possible to form a weakly connected graph, i.e. at least N-1 edges
    for k in range(min_k, len(possible_edges) + 1):
        # Generate all possible combinations of k edges
        edges_combinations = list(combinations(possible_edges, k))
        print(f"Edges combinations count: {len(edges_combinations)}")

        for edges in edges_combinations:
            # Create an empty candidate graph
            G_candidate = nx.DiGraph()

            # Print progress every 10 minutes
            current_time = time.time()
            if current_time - last_print_time >= 600:
                print(
                    f"Still generating subgraphs... Current time: {time.ctime(current_time)}"
                )
                last_print_time = current_time

            # Add nodes and edges to the candidate graph
            G_candidate.add_nodes_from(nodes)
            G_candidate.add_edges_from(edges)

            # Discard non-weakly connected graphs
            if not nx.is_weakly_connected(G_candidate):
                continue

            # Optimization #2: Pre-filter with invariants before full isomorphism test, as if the number of edges and the in/out degrees of the nodes do not match, the graphs cannot be isomorphic.
            cand_num_edges = G_candidate.number_of_edges()
            # Ensure degrees are calculated for all nodes, even isolated ones in a component
            cand_in_degrees = tuple(sorted(G_candidate.in_degree(n) for n in nodes))
            cand_out_degrees = tuple(sorted(G_candidate.out_degree(n) for n in nodes))

            is_isomorphic_found = False
            for motif_id in num_edges_to_motif_ids_map[cand_num_edges]:
                stored_graph, stored_in_degrees, stored_out_degrees = id_to_motif_map[
                    motif_id
                ]
                if (
                    cand_in_degrees == stored_in_degrees
                    and cand_out_degrees == stored_out_degrees
                ):
                    # Only if invariants match, run isomorphism test with vf2 algorithm.
                    if nx.is_isomorphic(G_candidate, stored_graph):
                        is_isomorphic_found = True
                        break

            if not is_isomorphic_found:
                id_to_motif_map[motifs_count] = (
                    G_candidate,
                    cand_in_degrees,
                    cand_out_degrees,
                )
                num_edges_to_motif_ids_map[cand_num_edges].append(motifs_count)
                motifs_count += 1

    return [
        motif_triplet[0] for motif_triplet in id_to_motif_map.values()
    ]  # Return only the graph objects

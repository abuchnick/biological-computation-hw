import argparse
import time

from common import MotifList, generate_motifs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n",
        type=int,
        nargs="+",
        required=False,
        help="Size of motifs (number of nodes) to generate.",
    )
    parser.add_argument(
        "--output-motifs",
        choices=["file", "console"],
        required=False,
        help="Output mode. If passed, the motifs will be written to a file or printed to the console.",
    )
    return parser.parse_args()


def prepare_textual_output(motifs: MotifList) -> str:
    """
    Prepare the textual output for the given list of motifs, according to the format specified in the assignment.
    Args:
        motifs: A list of motifs to be written to the output channel (file/console).
    Returns:
        The required textual output
    """
    motif_size = len(motifs[0].nodes)
    output = f"n={motif_size}\n"
    output += f"count={len(motifs)}\n"
    for i, motif in enumerate(motifs):
        output += f"#{i+1}\n"
        for j, edge in enumerate(motif.edges):
            output += f"{edge[0]} {edge[1]}"
            if not (i == len(motifs) - 1 and j == len(motif.edges) - 1):
                output += "\n"
    return output


def main(args: argparse.Namespace) -> None:
    """
    Traverse the given list of n values and generate the corresponding motifs for each n.
    For each n:
        - Generates all possible motifs of that size
        - Prints the time taken to generate the motifs, as well as the number of motifs generated
        - Outputs the motifs in the required format, according to the specified output mode.
    Raises:
        ValueError: If n is not provided
    Args:
        args: The parsed command-line arguments
    """
    n_values = args.n
    if n_values is None:
        raise ValueError("n must be provided")
    for n in n_values:
        print(f"Generating motif of size {n}...")
        start_time = time.time()
        print(f"Started at {time.ctime(start_time)}")
        motifs = generate_motifs(n)
        print(
            f"Generated {len(motifs)} motifs in {time.time() - start_time:.2f} seconds"
        )
        output_mode = args.output_motifs
        if output_mode is None:
            continue
        textual_output = prepare_textual_output(motifs)
        if output_mode == "file":
            with open(f"motifs_{n}.txt", "w") as f:
                f.write(textual_output)
        elif output_mode == "console":
            print(textual_output)


if __name__ == "__main__":
    args = parse_args()
    main(args)

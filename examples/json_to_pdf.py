from cgt_bandits import import_json
from cgt_bandits import export_dot
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python {sys.argv[0]} in.json out.pdf", file=sys.stderr)
        exit(1)

    with open(sys.argv[1], 'r') as file:
        game_string = file.read()

    root = import_json.json_to_nodes(game_string)
    dot = export_dot.nodes_to_dot(root)

    dot.write_pdf(sys.argv[2])

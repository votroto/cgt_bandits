import pygambit as pg
from cgt_bandits import import_efg
from cgt_bandits import export_dot
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: python {sys.argv[0]} in.efg out.pdf", file=sys.err)
        exit(1)

    g = pg.Game.read_game(sys.argv[1])

    si = import_efg.efg_to_nodes(g)
    go = export_dot.nodes_to_dot(si)

    go.write_pdf(sys.argv[2])

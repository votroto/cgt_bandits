import pygambit as pg
import cgt_bandits.import_efg
import cgt_bandits.export_dot
import sys

g = pg.Game.read_game(sys.argv[1])

si = import_efg.efg_to_nodes(g)
go = export_dot.nodes_to_dot(si)

go.write_pdf("tree.pdf")

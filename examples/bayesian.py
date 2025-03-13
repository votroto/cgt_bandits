from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
from cgt_bandits import export_efg
import pygambit


(a, b), (e, f) = (5, 2), (0, 2)
(c, d), (g, h) = (2, 1), (1, 4)

(A, B), (E, F) = (2, 0), (4, 0)
(C, D), (G, H) = (0, 1), (0, 2)


Lua, Lub, Ruc, Rud = (TerminalNode("Lua", [a, A]), TerminalNode("Lub", [b, B]), TerminalNode("Ruc", [e, E]), TerminalNode("Rud", [f, F]), )
Lda, Ldb, Rdc, Rdd = (TerminalNode("Lda", [c, C]), TerminalNode("Ldb", [d, D]), TerminalNode("Rdc", [g, G]), TerminalNode("Rdd", [h, H]), )


p2iflu = PersonalNode("", 2, 1, [Lua, Lub], ["a", "b"])
p2ifld = PersonalNode("", 2, 1, [Lda, Ldb], ["a", "b"])
p2ifru = PersonalNode("", 3, 1, [Ruc, Rud], ["c", "d"])
p2ifrd = PersonalNode("", 3, 1, [Rdc, Rdd], ["c", "d"])
p1ifl = PersonalNode("", 1, 0, [p2iflu, p2ifld], ["u", "d"])
p1ifr = PersonalNode("", 1, 0, [p2ifru, p2ifrd], ["u", "d"])

root = ChanceNode("Nature", [p1ifl, p1ifr], ["L", "R"], [3 / 4, 1 / 4])

efg = export_efg.nodes_to_efg(root, [0, 1])


import fractions

print(pygambit.nash.enumpure_solve(efg))


equilibrium = pygambit.nash.enummixed_solve(efg, rational=True)
# print(equilibrium.equilibria[0].payoff(efg.players[0]), file=sys.stderr)
for equil in equilibrium.equilibria:
    bb = equil.as_behavior()

    (x, y, z) = (
        bb[efg.players[0]][efg.infosets[0]],
        bb[efg.players[1]][efg.infosets[1]],
        bb[efg.players[1]][efg.infosets[2]],
    )
    x1, x2 = [fractions.Fraction(x.profile[action]) for action in x.infoset.actions]
    y1, y2 = [fractions.Fraction(y.profile[action]) for action in y.infoset.actions]
    z1, z2 = [fractions.Fraction(z.profile[action]) for action in z.infoset.actions]
    # ((x1, x2), (y1, y2), (z1, z2))
    #



    print(f"\\item $a_1$ --- {x._repr_latex_()};\\; $a_2$ --- {y._repr_latex_()}, {z._repr_latex_()}")
    print(f"\\item {equil.payoff(efg.players[0])._repr_latex_()}, {equil.payoff(efg.players[1])._repr_latex_()}")
    print(
       f"{x1:.2f},{x2:.2f} | [{y1:.2f}, {y2:.2f}],[{z1:.2f},{z2:.2f}]",
    )

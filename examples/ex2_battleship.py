from cgt_bandits.nodes import PersonalNode, TerminalNode
from cgt_bandits import export_dot

# WARNING: This game is too big to export as Gambit EFG or PDF.
# Do not try. :)

# Players place a single 2x1 battleship on a 2x2 map, then take turns
# trying to guess the opponent battleship's position and sink it.


def valid_placements():
    positions = []

    for i in range(2):
        for j in range(1):
            positions.append([(i, j), (i, j + 1)])
            positions.append([(j, i), (j + 1, i)])

    return positions


def valid_targets(shots):
    return [(i, j) for i in range(2) for j in range(2) if (i, j) not in shots]


def scored_hits(placement, shots):
    return [shot for shot in shots if shot in placement]


def is_sunk(placement, shots):
    return all(section in shots for section in placement)


def knowledge_0(ship0, ship1, shot0, shot1):
    # Players know their own ship position, the shots taken by both players,
    # and which of their own shots were successful hits.

    boom = scored_hits(ship1, shot0)
    info = (tuple(ship0), tuple(shot0), tuple(shot1), tuple(boom))

    return hash(info)


def knowledge_1(ship0, ship1, shot0, shot1):
    boom = scored_hits(ship0, shot1)
    info = (tuple(ship1), tuple(shot0), tuple(shot1), tuple(boom))

    return hash(info)


def shoot_0(ship0, ship1, shot0=[], shot1=[]):
    # Main loop of the game: Take turns guessing where the oponent's ship is.
    # Game ends as soon as any ship is sunk.

    if is_sunk(ship0, shot1):
        return TerminalNode("P0 lost", [-1, 1])

    opts = valid_targets(shot0)
    infoset = knowledge_0(ship0, ship1, shot0, shot1)
    actions = [str(o) for o in opts]
    children = [shoot_1(ship0, ship1, shot0 + [tgt], shot1) for tgt in opts]

    return PersonalNode("shoot", infoset, 0, children, actions)


def shoot_1(ship0, ship1, shot0=[], shot1=[]):
    if is_sunk(ship1, shot0):
        return TerminalNode("P1 lost", [1, -1])

    opts = valid_targets(shot1)
    infoset = knowledge_1(ship0, ship1, shot0, shot1)
    actions = [str(o) for o in opts]
    children = [shoot_0(ship0, ship1, shot0, shot1 + [tgt]) for tgt in opts]

    return PersonalNode("shoot", infoset, 1, children, actions)


def place_0():
    # Pick one of the 4 valid ship placements

    placements = [p for p in valid_placements()]
    actions = [str(o) for o in placements]
    children = [place_1(ship) for ship in placements]

    return PersonalNode("place", 0, 0, children, actions)


def place_1(ship0):
    placements = [p for p in valid_placements()]
    actions = [str(o) for o in placements]
    children = [shoot_0(ship0, ship1) for ship1 in placements]

    return PersonalNode("place", 0, 1, children, actions)


if __name__ == "__main__":
    dot = export_dot.nodes_to_dot(place_0())
    print(dot)

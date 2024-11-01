from cgt_bandits.utils import fixup_nodes


def nodes_to_efg(root, players, name=""):
    # EFG is too slow for BRUTE, let's try this instead.

    return fixup_nodes(root)

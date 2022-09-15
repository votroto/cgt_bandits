import unittest
from cgt_bandits.nodes import ChanceNode, PersonalNode, TerminalNode
from cgt_bandits import export_efg

def build_example():
    probs = [0.5, 0.5, 0.0]
    names = ["1", "2", "3"]
    terms = [
        TerminalNode("t1", [0, 1]),
        TerminalNode("t2", [0, 2]),
        TerminalNode("t3", [0, 3]),
    ]
    root = ChanceNode("c", terms, names, probs)

    efg = export_efg.nodes_to_efg(root)
    return repr(efg)


expected_efg = '''EFG 2 R "" { "p1" "p2" }
""

c "c" 1 "" { "1" 0.5 "2" 0.5 "3" 0 } 0
t "t1" 1 "" { 0, 1 }
t "t2" 2 "" { 0, 2 }
t "t3" 3 "" { 0, 3 }
'''

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual(build_example(), expected_efg)

if __name__ == '__main__':
    unittest.main()
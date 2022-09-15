# Bandits Tree
Tools for the Bandits Tree homework.

## Examples
Examples in the `examples` directory show how to build a simple poker game, how to export it as a gambit `efg` file, and how to draw a game tree as a `pdf`.

You need `graphviz` (https://www.graphviz.org/download/) to visualize games.

```sh
# To build a simple poker game and output it into an efg file:
python test_poker.py > poker.efg

# To draw any efg file as a pdf:
python efg_to_pdf.py poker.efg poker.pdf
```
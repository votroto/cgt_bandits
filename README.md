# Extensive Form Games: Bandits
Tools for the Bandits Tree homework.

## Installation
Install the package directly from Github.
```
pip install git+https://github.com/votroto/cgt_bandits.git
```

### PDF Output
The `dot` command from Graphviz is used to render the games as PDFs and must be [installed separately](https://www.graphviz.org/download/).

## Examples
Examples in the `examples` directory show how to build a simple poker game, how to export it as a gambit `efg` file, and how to draw a game tree as a `pdf`.

```sh
# To build a simple poker game and output it into an efg file:
python ex0_poker.py > poker.efg

# To draw any efg file as a pdf:
python efg_to_pdf.py poker.efg poker.pdf
```
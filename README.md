# Extensive Form Games: Bandits
Tools for the Bandits Tree homework. For creating Extensive form games, then exporting and importing them as the following formats:
* **EFG** (Gambit support)
* **DOT** (rendering)
* **JSON**


## Installation
Install the package directly from Github.
```
pip install git+https://github.com/votroto/cgt_bandits.git[dot,gambit]
```
Including the support for *Graphviz* (`dot`) visualizations and the *Gambit* game-theory tools is recommended.

### PDF Output
The `dot` command from *Graphviz* is used to render the games as PDFs and must be [installed separately](https://www.graphviz.org/download/).


## Examples
Examples in the `examples` directory show how to build simple games, how to export them as gambit JSON, and how to render a game tree as a PDF.

Build a simple poker game and dump it as JSON:
```sh
python ex0_poker.py > poker.json
```

Use `export_dot` to render a game as a PDF directly:
```sh
# Assuming root contains your game
dot = export_dot.nodes_to_dot(root)
dot.write_pdf("filename.pdf")
```

Use the `json_to_pdf.py` example application, if you already have games in either JSON or the standard EFG format:
```sh
python json_to_pdf.py game.json game.pdf
```

## Development
Contributions are welcome. Fork the repository on GitHub, then
```sh
# Clone the repository
git clone git@github.com:USERNAME/cgt_bandits.git
# Install an editable version with dev dependencies
pip install -e ./cgt_bandits[dev]
# Make changes... and test
pytest tests
```

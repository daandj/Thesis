# Readme

## Setup

To use the code and recreate the experiments you first have to package and install `cbt` locally.

First download the code by cloning the repository:
```sh
git clone https://github.com/daandj/Thesis
cd Thesis
```

Then activate the venv and build the package
```sh
soure .venv/bin/activate
pip install -e .
```

Now you should be able to import the package in a python script as usual:
```python
from cbt.games.tictactoe import TicTacToe

ttt = TicTacToe()
```
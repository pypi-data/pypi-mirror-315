## jupyter-play 


This package contains a number of basic HTML/CSS/JS games you can play in your jupyter notebook! 

All credit for making the original game files goes to [Steven Lambert](https://gist.github.com/straker).

![snake_preview.gif](snake_preview.gif)

### Installation

```bash 
pip install jupyter-play
```

I recommend [uv](https://docs.astral.sh/uv/) to all python users for managing their dependencies and virtual environments.

```bash
uv init # optional, creates a pyproject.toml 
uv venv --python 3.11 
source .venv/bin/activate
uv add --group fun jupyter-play # e.g. add a "fun" group under your development dependencies
```

The package source distribution includes a `.zip` of html games to play. `setup.py` includes a custom build step to unzip the game files from this `html_games.zip`; this means the files are unzipped in the installed version of the package (the "wheel"). More information on source distributions vs wheels can be found [here](https://packaging.python.org/en/latest/discussions/package-formats/#package-formats).

- *To packaging workshop attendees (12/20/24):* see if you can figure out how to exclude `.zip` from the installed state!

`download_games.sh` is the script to download and zip the game files from the original github gists. 

### Usage 

```python 
## in an .ipynb file

from jupyter_play import PLAY

# View the list of games included
print(PLAY.list_games())

# Play any game you like
PLAY.SNAKE()
```

You can also run your own games (right now just from a string)

```python 
# Play your own game (load to string first)
from jupyter_play import play
with open('my_one_file_game.html', 'r') as file: 
    game_html = file.read()
play(game_html)
```

Please note that this package is only meant to work with basic, self-contained, one-file `.html` games in a jupyter notebook environment (i.e. with a running ipykernel).

### Contributing 

The games' creator intentionally left some core features lacking as an exercise for the reader. I may be making some of these additions myself, but if you're excited to contribute yourself please feel free to open a PR and edit one of the base game files in `source_games`.

I have other ideas for feature additions as well: 

* Basic AIs to play the games for you in a screensaver-like fashion.
* Configure difficulty and speed settings. 
* Introduce new games.
* Add new levels (procedurally generated?)
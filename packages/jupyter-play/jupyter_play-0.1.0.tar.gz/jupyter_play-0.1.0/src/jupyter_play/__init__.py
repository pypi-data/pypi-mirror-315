
from IPython.display import display, HTML
import importlib.resources as pkg_resources
import os
import functools
from types import FunctionType
import logging 
import inspect

logger = logging.getLogger(__name__)

def load_html_files() -> dict[str, str]: 
    """
    Loads a dict of html file names and contents from package resources.
    """
    html_files = {}
    html_package = 'jupyter_play.html_games'
    try: 
        for file_name in pkg_resources.contents(html_package):
            if file_name.endswith('.html'): 
                with pkg_resources.open_text(html_package, file_name) as file: 
                    html_files[file_name] = file.read()
    except ModuleNotFoundError: 
        logger.error(f'Failed to find {html_package} in package resources. Check that the package was built correctly.')

    return html_files

def play(html: str) -> None:
    """
    Play a simple html-based game in the display window under a jupyter notebook cell.
    """
    display(HTML(html))

def _run_html(file_name: str, game_dir: dict[str, str] = load_html_files()) -> None:
    """
    Load and run an html file from package resources
    """
    if game := game_dir.get(file_name, None): 
        play(game)
    else: 
        logger.error(f'Failed to find {file_name} in package resources. Check that the package was built correctly')

class PLAY: 
    SNAKE = functools.partial(_run_html, 'snake.html')
    PONG = functools.partial(_run_html, 'pong.html')
    TETRIS = functools.partial(_run_html, 'tetris.html')
    BOMBERMAN = functools.partial(_run_html, 'bomberman.html')
    BREAKOUT = functools.partial(_run_html, 'breakout.html')
    FROGGER  = functools.partial(_run_html, 'frogger.html')
    MISSILE_COMMAND = functools.partial(_run_html, 'missile-command.html')
    SOKOBAN = functools.partial(_run_html, 'sokoban.html')
    DOODLE_JUMP = functools.partial(_run_html, 'doodle-jump.html')
    PUZZLE_BOBBLE = functools.partial(_run_html, 'puzzle-bobble.html')
    HELICOPTER = functools.partial(_run_html, 'helicopter.html')
    # BLOCK_DUDE = functools.partial(_run_html, 'block-dude.html')

    @classmethod
    def list(cls) -> list:
       return [g for g in vars(cls) if g != 'list' and not g.startswith('__')]


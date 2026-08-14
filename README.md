# Alien Invasion

Alien Invasion is a complete arcade shooter built with Python and Pygame. Clear
each descending fleet before it reaches your ship. Every cleared wave moves
faster and awards more points.

## Run the game

The project uses [uv](https://docs.astral.sh/uv/) to manage its environment:

```bash
uv sync
uv run python alien_invasion.py
```

Alternatively, install `pygame>=2.6.1` in a Python 3.10-3.13 environment and
run `python alien_invasion.py`.

## Controls

| Action | Control |
| --- | --- |
| Move | Left/Right arrows or A/D |
| Fire | Space |
| Start/restart | Enter or the Play button |
| Pause | P |
| Quit | Escape or Q |

You begin with three ships. The HUD shows the current wave, session high score,
current score, and remaining ships. The window can be resized at any time and
keeps the active fleet and HUD fitted to the available play area.

## Tests

```bash
uv run python -m unittest discover -s tests -v
```

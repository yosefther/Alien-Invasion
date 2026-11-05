# Alien Invasion

An arcade shooter in Python and Pygame. Shoot down each fleet before it reaches your ship. Every wave you clear moves faster and is worth more points.

## How to run it

Python 3.10–3.13 with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run python alien_invasion.py
```

Or install `pygame>=2.6.1` yourself and run `python alien_invasion.py`.

| Action | Keys |
| --- | --- |
| Move | Left/Right or A/D |
| Fire | Space |
| Start / restart | Enter or click Play |
| Pause | P |
| Quit | Esc or Q |

You get three ships. The HUD shows the wave, score, session high score and ships left.

## How it works

`alien_invasion.py` runs the main loop and owns the game state. Ships, aliens and bullets are Pygame sprites, and hits come from `pygame.sprite.groupcollide`. When a fleet is cleared, `Settings.increase_speed()` multiplies alien speed by 1.14 and points by 1.35, so later waves get harder and pay more.

The window is resizable. On resize the ship, HUD, bullets and aliens are rescaled to the new play area, so the current game keeps going instead of restarting. There's a minimum size of 800×600.

## Tests

```bash
uv run python -m unittest discover -s tests -v
```

The tests run headless (SDL dummy driver). They cover ship bounds, the bullet limit, collisions and scoring, wave progression, game over, rendering and resizing.

## License

MIT. See [LICENSE](LICENSE).

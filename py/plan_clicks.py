"""How many clicks a plan makes, and on which ticks.

A click is player 1's button going down: an `input=<tick>,<buttons>` line whose bit 0 is
set when the line before it had bit 0 clear. Holding through several jumps is one click.
leveldp prints the same count as `clicks:` under --minclicks; this reads it off any plan
file, including a solution the loop assembled from several solves and splices, which no
single solver call saw whole.

    python py/plan_clicks.py <plan> [<plan> ...]   # one line per file
    python py/plan_clicks.py --ticks <plan>        # ...and the tick of every press
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from splice_plan import read


def presses(edges: list[tuple[int, int]]) -> list[int]:
    """The ticks the button goes down on. A plan starts released (the solver's t=0)."""
    out, prev = [], 0
    for tick, level in edges:
        if (level & 1) and not (prev & 1):
            out.append(tick)
        prev = level
    return out


def main(argv: list[str]) -> int:
    ticks = "--ticks" in argv
    paths = [a for a in argv if a != "--ticks"]
    if not paths:
        print(__doc__.strip())
        return 2
    for p in paths:
        edges = read(Path(p))
        t = presses(edges)
        print(f"{p}: {len(t)} clicks, {len(edges)} edges"
              + (f", presses t={t[0]}..{t[-1]}" if t else ""))
        if ticks:
            print(" ".join(str(x) for x in t))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

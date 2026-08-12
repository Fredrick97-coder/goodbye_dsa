#!/usr/bin/env python3
"""
Generate the confetti Lottie animation.

Why generate it rather than download one:

* **Palette.** The confetti uses this app's own colours (volt, mint, amber, sky,
  rose) rather than whatever a stock asset ships with, so the celebration looks
  like part of the product instead of a sticker on top of it.
* **Licensing.** A hand-generated file has no attribution question attached.
* **Control.** Particle count, gravity, spin and duration are parameters here,
  so tuning the feel is editing three numbers and re-running, not hunting for a
  different asset.

The motion is a real projectile simulation -- launch velocity, gravity, and air
drag -- sampled into position keyframes. Expressing gravity through bezier
easing would be guesswork; sampling an actual trajectory looks right because it
*is* right.

Two cannons fire from the bottom corners toward the middle, which is the "split"
burst: the screen fills from both sides at once rather than from a single point.

    python3 scripts/gen_confetti.py          # writes src/assets/confetti.json
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "src" / "assets" / "confetti.json"

# ----------------------------------------------------------------- knobs

WIDTH, HEIGHT = 1600, 900
FPS = 60
DURATION_FRAMES = 132              # 2.2 seconds: long enough to read as a
                                   # celebration, short enough not to be in the
                                   # way of reading the test results
PARTICLES_PER_CANNON = 60          # 34 read as "some paper fell", not a burst
SAMPLE_EVERY = 6                   # frames between position keyframes
LAUNCH_JITTER = 10                 # frames: a perfectly simultaneous launch
                                   # looks mechanical

# Tuned against the canvas, not guessed: at the previous 2400 px/s the apex was
# ~1900 px above a 900 px canvas, so the fastest half of the confetti left the
# screen entirely and the middle of the animation looked empty. Slower launch
# plus stronger gravity keeps the arc inside the frame.
GRAVITY = 2400.0                   # px/s^2
DRAG = 0.9                         # velocity retained per second: paper does not
                                   # keep its launch speed
SPEED_MIN, SPEED_MAX = 1000.0, 1900.0

#: The app's palette, from tailwind.config.js. White is included because a few
#: pale flecks stop the whole burst reading as one hue.
COLORS = [
    "#6d4aff", "#8a6dff", "#a894ff",     # volt
    "#2ed3a0", "#12b981",                # mint
    "#ffbe4d", "#f5a524",                # amber
    "#54b3f5", "#2c9ceb",                # sky
    "#ff6b88",                           # rose
    "#e6ebf4",                           # mist
]

EASE_OUT = {"i": {"x": [0.25], "y": [1]}, "o": {"x": [0.35], "y": [0]}}


def rgb(hex_colour: str) -> list:
    """Lottie wants normalised RGBA."""
    h = hex_colour.lstrip("#")
    return [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)] + [1]


def linear_kf(t: int, value: list) -> dict:
    """
    A keyframe with linear interpolation to the next one.

    Values are rounded to integers: sub-pixel precision in a 1600px canvas that
    is then scaled to the viewport is noise, and it costs a tenth of the file.
    """
    return {"i": {"x": [1], "y": [1]}, "o": {"x": [0], "y": [0]},
            "t": t, "s": [round(v) for v in value]}


def simulate(x0: float, y0: float, angle: float, speed: float) -> list:
    """
    Sample a trajectory into (frame, [x, y]) pairs.

    Drag is applied per frame as an exponential decay so it is frame-rate
    independent, and the vertical component keeps accelerating under gravity --
    which is what gives confetti its slow hang at the top of the arc.
    """
    vx = math.cos(angle) * speed
    vy = -math.sin(angle) * speed          # Lottie's y grows downward
    x, y = x0, y0
    dt = 1.0 / FPS
    decay = DRAG ** dt
    points = [(0, [x, y])]
    for frame in range(1, DURATION_FRAMES + 1):
        vx *= decay
        vy = vy * decay + GRAVITY * dt
        x += vx * dt
        y += vy * dt
        if frame % SAMPLE_EVERY == 0 or frame == DURATION_FRAMES:
            points.append((frame, [x, y]))
    return points


def particle_layer(index: int, rng: random.Random, from_left: bool) -> dict:
    delay = rng.randint(0, LAUNCH_JITTER)
    # Cannons sit just off-screen at the bottom corners, so particles appear to
    # be fired in from outside rather than spawning in view.
    x0 = -40.0 if from_left else WIDTH + 40.0
    y0 = HEIGHT + 30.0

    # Aimed up and inward, with a wide spread. 55-105 degrees from horizontal.
    spread = math.radians(rng.uniform(55, 105))
    angle = spread if from_left else math.pi - spread
    speed = rng.uniform(SPEED_MIN, SPEED_MAX)

    points = [(t + delay, p) for t, p in simulate(x0, y0, angle, speed)]
    position_kfs = [linear_kf(t, p) for t, p in points]
    # The last keyframe holds, so it needs no easing pair.
    position_kfs[-1] = {"t": points[-1][0],
                        "s": [round(v) for v in points[-1][1]]}

    # Spin: a few full turns, direction and rate varying per particle.
    turns = rng.uniform(1.5, 4.0) * rng.choice((-1, 1))
    rotation = {"a": 1, "k": [
        {**EASE_OUT, "t": delay, "s": [round(rng.uniform(0, 360), 1)]},
        {"t": DURATION_FRAMES, "s": [round(turns * 360, 1)]},
    ]}

    # Flutter: squashing the x scale reads as a flat rectangle turning edge-on.
    # This is the difference between confetti and falling dots.
    flutter, phase = [], rng.randint(0, 3)
    steps = 6
    for step in range(steps + 1):
        t = delay + round(step * (DURATION_FRAMES - delay) / steps)
        sx = 100 if (step + phase) % 2 == 0 else rng.uniform(15, 45)
        flutter.append(linear_kf(t, [sx, 100, 100]))

    # Fade only at the very end: fading throughout makes the burst look weak.
    fade_start = int(DURATION_FRAMES * 0.72)
    opacity = {"a": 1, "k": [
        linear_kf(delay, [100]),
        linear_kf(fade_start, [100]),
        {"t": DURATION_FRAMES, "s": [0]},
    ]}

    w = rng.uniform(9, 16)
    h = rng.uniform(14, 26)

    return {
        "ddd": 0, "ind": index, "ty": 4, "nm": f"c{index}", "sr": 1,
        "ks": {
            "o": opacity,
            "r": rotation,
            "p": {"a": 1, "k": position_kfs},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {"a": 1, "k": flutter},
        },
        "ao": 0,
        "shapes": [{
            "ty": "gr", "nm": "g", "np": 2, "cix": 2, "ix": 1, "bm": 0, "hd": False,
            "it": [
                {"ty": "rc", "d": 1, "nm": "r", "hd": False,
                 "s": {"a": 0, "k": [round(w, 1), round(h, 1)]},
                 "p": {"a": 0, "k": [0, 0]},
                 "r": {"a": 0, "k": 2}},
                {"ty": "fl", "nm": "f", "hd": False, "r": 1, "bm": 0,
                 "c": {"a": 0, "k": rgb(rng.choice(COLORS))},
                 "o": {"a": 0, "k": 100}},
                {"ty": "tr", "nm": "t",
                 "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0},
                 "o": {"a": 0, "k": 100}, "sk": {"a": 0, "k": 0},
                 "sa": {"a": 0, "k": 0}},
            ],
        }],
        # `ip` is the layer's in-point: a staggered particle simply does not
        # exist until its cannon fires, rather than sitting visible at the
        # muzzle waiting.
        "ip": delay, "op": DURATION_FRAMES, "st": 0, "bm": 0,
    }


def build() -> dict:
    # Seeded, so regenerating produces an identical file and the diff is empty
    # unless a knob above actually changed.
    rng = random.Random(20260812)
    layers = []
    index = 1
    for from_left in (True, False):
        for _ in range(PARTICLES_PER_CANNON):
            layers.append(particle_layer(index, rng, from_left))
            index += 1
    return {
        "v": "5.9.0", "fr": FPS, "ip": 0, "op": DURATION_FRAMES,
        "w": WIDTH, "h": HEIGHT, "nm": "forge-confetti", "ddd": 0,
        "assets": [], "fonts": {"list": []}, "layers": layers, "markers": [],
    }


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = build()
    OUT.write_text(json.dumps(data, separators=(",", ":")))
    size = OUT.stat().st_size
    print(f"wrote {OUT.relative_to(Path.cwd())}: {len(data['layers'])} particles, "
          f"{size:,} bytes ({size / 1024:.0f} KB)")

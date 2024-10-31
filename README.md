# bb

This is a tiny project to generate fully functional deep groove ball bearings via Python. This is a small example of OAC (Object As Code) and parametric cad design.

To create a bearing, simply run `basic.py`. It's recommended to use `uv` as it will manage the environment for you (built for OSX ARM users)

```bash
uv run basic.py
# CAD env loaded
# BearingConfig(number_of_balls=8, circle_radius=20, ball_diameter=4.1, thickness=4)
# <bb.BearingBuilder object at 0x104725750>
# Start export
# SVG export time:  18.24527883529663
```

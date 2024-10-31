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


## Generated `.3mf`

<img width="582" alt="3mfout" src="https://github.com/user-attachments/assets/cf85ef14-9c94-47e6-89f5-5b940a096ab1">


## Printed and spinning

https://github.com/user-attachments/assets/f42e9984-a9ab-4f14-ae13-d7c7fda380cd


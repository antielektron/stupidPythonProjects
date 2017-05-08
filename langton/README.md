# Langton's Ant Simulator

```
usage: Main.py [-h] [--steps STEPS] [--w W] [--h H] [--calc CALC]
               [--default DEFAULT] [--fullscreen] [--window_w WIN_W]
               [--window_h WIN_H] [--configurator] [--code CODE]

langton's ant

optional arguments:
  -h, --help         show this help message and exit
  --steps STEPS      steps per second
  --w W              field width
  --h H              field height
  --calc CALC        calculate steps and only display result
  --default DEFAULT  setting all fields to this value
  --fullscreen
  --window_w WIN_W   window width
  --window_h WIN_H   window height
  --configurator     start in field edit mode
  --code CODE        binary code for the ant ('01' corresponds to the
                     starndard ant behaviour)

```

configuration mode keys:

| key        | function                               |
| ---------- | -------------------------------------- |
| return     | enter/leave configuration mode         |
| arrow keys | move langton's ant                     |
| space      | activate field or switch field's color |
| backspace  | deactivate field                       |
| escape     | exit program                           |


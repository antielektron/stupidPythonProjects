# Langton's Ant Simulator

```
usage: Main.py [-h] [--steps STEPS] [--w W] [--h H] [--calc CALC]
               [--fullscreen] [--window_w WIN_W] [--window_h WIN_H]
               [--configurator] [--code CODE] [--pattern PATTERN]

langton's ant simulation tool

optional arguments:
  -h, --help         show this help message and exit
  --steps STEPS      steps per second
  --w W              field width
  --h H              field height
  --calc CALC        calculate steps and only display result
  --fullscreen
  --window_w WIN_W   window width
  --window_h WIN_H   window height
  --configurator     start in field edit mode
  --code CODE        binary code for the ant ('01' corresponds to the starndard ant behaviour)
  --pattern PATTERN  initial pattern for the field. Possible values:
                     	 * 0: all fields inactive
                     	 * 1: all fields active
                     	 * check: checkboard pattern
                     	 * horizontal: horizontal stripes
                     	 * vertical: vertical stripes
                     	 * random: random values

```

keys:

| key                    | function                                 |
| ---------------------- | ---------------------------------------- |
| return                 | enter/leave configuration mode           |
| arrow keys             | move langton's ant (in configuration mode) |
| space                  | activate field or switch field's color (in configuration mode) |
| backspace              | deactivate field (in configuration mode) |
| ctrl left / ctrl right | rotate ant (in configuration mode)       |
| escape                 | exit program                             |


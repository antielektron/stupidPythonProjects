# Evolutionary Algorithm Simulator

##  run the program:

```
usage: main.py [-h] [--offspringSize OFFSPRINGSIZE] [--P P] [--L L] [--f F]
               [--epsilon EPSILON] [--cycles CYCLES]

evolutionary algorithm simulation

optional arguments:
  -h, --help            show this help message and exit
  --offspringSize OFFSPRINGSIZE
                        size for new offspring
  --P P                 start population size
  --L L                 genome length
  --f F                 fitness function in python syntax. x[0] - x[L] are the arguments
  --epsilon EPSILON     epsilon for random mutation
  --cycles CYCLES       cycles to calculate

```

arguments can also be adjusted by the user at runtime. Example for a 2 dimensional fitness function:

```
./main.py --f "-abs(x[0] - 6) - abs(x[1] +5)" --L 2 --cycles 1000
```


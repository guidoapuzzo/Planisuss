# Planisuss

An **artificial-ecosystem simulation** in Python, inspired by Wa-Tor and Conway's Game of Life, with an interactive Matplotlib visualisation and an MVC architecture.

> University programming project.

## The world

A grid of cells, each either water or land. Land cells can host three species:

- **Vegetob**: a plant species that grows every day and feeds the herbivores.
- **Erbast**: herbivores that graze Vegetob and move in search of better living conditions, organised in **herds**.
- **Carviz**: carnivores that hunt Erbast and form social groups called **prides**.

## Simulation dynamics

- **Daily cycle**: growth, movement, grazing, hunting and reproduction happen in phases every day.
- **Social groups**: herds and prides influence individual choices, such as moving with the group or splitting from it.
- **Energy and lifespan**: individuals gain energy by eating and lose it by moving and fighting. When energy runs out or the lifespan ends, they die.
- **Predation and reproduction** follow rules based on energy and age.
- **Ecosystem balance**: constants (grid size, herd size, energy limits, lifespan) prevent overpopulation and extinction.
- **Terrain generation** with Perlin noise.

## Features

- Animated, interactive visualisation (Matplotlib animation, slider and buttons).
- Population statistics during the simulation.
- Save and reload of the simulation state (`pickle`).

## Architecture

Model-View-Controller:

```
├── main.py                       # entry point
├── constants.py                  # simulation parameters
├── Model/
│   ├── CellModel.py              # grid cells (land / water)
│   ├── Creatures.py              # Vegetob, Erbast, Carviz
│   ├── Herd.py                   # Erbast herds
│   └── Pride.py                  # Carviz prides
├── Controller/
│   ├── SimulationController.py   # daily cycle and rules
│   └── DataPersistence.py        # save / load
└── View/
    └── Simulator.py              # Matplotlib visualisation
```

## How to run

```bash
pip install -r requirements.txt
python main.py
```

Simulation parameters (grid size, number of days, lifespans) can be changed in `constants.py`.

## Tech stack

Python · NumPy · Matplotlib · noise (Perlin noise)

## License

Released under the [MIT License](LICENSE).

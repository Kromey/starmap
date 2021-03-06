# Hyperspace Network Simulation

This program is intended to simulate the exploration of hyperspace and expansion of the hyperspace network for the science-fiction world of [Exogenesis]. The star catalog in use is the HabHYG dataset, compiled by [Winchell Chung][habhyg].

## Prerequisites

This simulation is written for Python 3. It is recommended to use a virtual environment, and then install the prerequisites:

```bash
$ pip install -r requirements.txt
```

## Running the simulation

```bash
$ python run_simulation.py
```

Simulation results are saved as CSV in `routes.csv`.

## Generating the starmap

After you have run the simulation, or otherwise obtained a `routes.csv` file,
you can generate the 2D starmap with the following command:

```bash
$ python draw_map.py
```

[exogenesis]: https://world.payloadgame.dev/
[habhyg]: http://www.projectrho.com/public_html/starmaps/catalogues.php#id--Catalogues--HabHYG

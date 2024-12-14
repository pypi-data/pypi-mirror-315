# Call Shot to the Nuts

PyCallShot is a simple independent Python library for rolling dice and managing dice rolls in your games and applications.

## Features

- Roll any number and type of dice (d4, d6, d20, d69 etc.)
- Support for complex dice mechanics:
  - Advantage/disadvantage rolls
  - Exploding dice
  - Success thresholds and hit count a-la Shadowrun and WoD
  - Dice and result modifiers
  - Subtract ones (for specific game systems)
- Roll logging capability
- Reproducible results with seed support
- Save and load frequently used roll configurations

## Installation

```bash
pip install pycallshot
```

## Quick Start

```python
import pycallshot as cs

# Create a dice tower object that holds config data, last roll, and
# provides methods for rolling, loading and saving rolls
# (optional seed for reproducibility)
tower = cs.DiceTower(seed=None, log=False)

# Simple d20 roll with 4 added to result
roll = cs.Roll._from_notation('d20+4')  # 1d20+4
result = tower.roll(roll)

# Complex roll with multiple dice
complex_roll = cs.Roll(
    pool=8,        # Number of dice
    d=6,           # Six-sided dice
    threshold=5,   # Count successes for rolls >= 5
    explode=6,     # On 6s, keep result and roll again
    subtractOnes=False,  # Don't subtract 1s from success count
    diceMod=0,     # No modifier to individual dice
    resultMod=0,   # No modifier to final result
    adv=0          # No advantage/disadvantage
)
result = tower.roll(complex_roll)
```

## Detailed Usage

### Creating Rolls

There are two ways to create a roll:

1. Using the constructor:
```python
roll = cs.Roll(
    pool=3,        # Number of dice
    d=4,           # Die sides
    resultMod=4    # Add 4 to final result
)
```

2. Using notation (similar to standard RPG notation):
```python
roll = cs.Roll._from_notation('d20adv')  # d20 with advantage
roll = cs.Roll._from_notation('2d6+4')   # 2d6 plus 4
```

### Using the Dice Tower

The DiceTower class handles the execution of rolls:

```python
# Create a tower with logging enabled
tower = cs.DiceTower(seed=None, log=True)

# Roll the dice
result = tower.roll(roll)

# Re-roll the last roll
new_result = tower.reroll()

# Save frequently used rolls
tower.save(roll, 'attack_roll')

# List saved rolls, wait for input to select one of the rolls, and use selected roll
result = tower.from_loaded()

```

### Roll Parameters

- `pool`: Number of dice to roll
- `d`: Number of sides on each die
- `threshold`: Success threshold for counting hits
- `explode`: Value at which dice "explode" (roll again)
- `subtractOnes`: Whether to subtract ones from success count
- `diceMod`: Modifier added to each individual die
- `resultMod`: Modifier added to final result
- `adv`: Advantage (1), Disadvantage (-1), or Normal (0)

### Notation
The notation string takes the following details:
- `dX` - X-sided dice
- `Yd` - the value to the left of `d` is always the the number of dice to roll
- `adv` - roll with advantage
- `dis` - roll with disadvantage
- `!X` - explode values of X or higher
- `tX` - success threshold X
- `s` - subtract ones from success count
- `+X` - add X to the end result of roll
- `-X` - subtract X from the end result of roll
Adding modifiers to each die is not supported in notation. Use the `diceMod` parameter instead.

## Logging

Enable logging to keep track of all rolls:

```python
tower = cs.DiceTower(log=True)
```

Logs will be saved to `log.txt` with timestamps and detailed roll information.

## Storing and Loading Rolls with CSV file

The `to_csv` and `from_csv` methods can be used to save and load rolls to and from a CSV file.
To get the headers to manually set up rolls, run to_csv once. Default path is `saved_rolls.csv`.
Running from_csv will overwrite the rolls currently stored in memory. Writing to_csv will overwrite existing file.
Thought about using Pandas for some fancy exporting and sorting, opted to keep independent for such a small project.

## Contributing

Contributions are welcome! This is a learning project, so please feel free to make changes and submit feedback.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

Dmitry Hayday

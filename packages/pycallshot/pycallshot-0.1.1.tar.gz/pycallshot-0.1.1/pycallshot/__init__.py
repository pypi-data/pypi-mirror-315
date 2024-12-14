"""
PyCallShot - A Python library for rolling dice and managing dice rolls.
"""

from .dice_tower import DiceTower
from .roll import Roll
from typing import List, Dict, Tuple, Set, Optional, TypeVar, Union
from dataclasses import dataclass
import random as rnd

__version__ = "0.1.1"
__all__ = ["DiceTower", "Roll"]

LastRoll = Roll(1, 20)
LoadedRolls = {}
RollHistory = []

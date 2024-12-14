"""
Roll class for storing dice rolls.
It supports 2 initialization methods:
- Roll(pool, d, threshold=0, explode=0, subtractOnes=False, diceMod=0, resultMod=0, adv=0)
- Roll._from_notation(notation)

Examples:
- .Roll(8, 6, explode=6, threshold=5) - 8 d6 dice, explode 6 or higher, success threshold 5
- ._from_notation('d20+4adv') - roll 1 d20 with advantage and add 4 to result
- '2d6+4' - roll 2 d6 and add 4 to result

Note that this is a dataclass used for storing dice rolls. It does not perform any roll logic.
To get roll results, pass the roll to the DiceTower class. See the DiceTower class for more information. 
"""
from typing import List, Dict, Tuple, Set, Optional, TypeVar, Union
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Roll:
    """A class that represents a dice roll."""
    
    d: int
    threshold: int
    pool: int
    explode: int
    subtractOnes: bool
    diceMod: int
    resultMod: int
    adv: int
    description: str = ''
    name: str = ''

    def __init__(self, pool: int, d: int, *, threshold: int = 0, explode: int = 0, subtractOnes: bool = False, diceMod: int = 0, resultMod: int = 0, adv: int = 0, name: str = ''):        
        """
        Initialize a new Roll instance.
        Args:
            pool            - required, int:            the number of dice to roll at a time 
            d               - required, int:            number of die sides (e.g. 6 for a common board game die)
            threshold       - optional, default 0:      the threshold of success/hit on a single die. If 0, then no checks are performed 
            explode         - optional, default 0:      if set higher than 0, keeps roll result and rolls again if result > threshold 
            subtractOnes    - optional, default False:  if True, then all dice that rolled 1s are counted against the total number of hits. 
            diceMod         - optional, default 0:      adds or subtracts from each die roll
            resultMod       - optional, default 0:      adds or subtracts from the total result
            adv             - optional, default 0:      1 to roll with advantage, -1 to roll with disadvantage, 0 to roll normally
            name            - optional, default '':     name of the roll. If empty, generates a timestamp-based name
        """
        self.d = d
        self.threshold = threshold
        self.pool = pool
        self.explode = explode
        self.subtractOnes = subtractOnes
        self.diceMod = diceMod
        self.resultMod = resultMod
        self.adv = adv
        self.description = ''
        # Generate timestamp name only if no name provided
        self.name = name if name != '' else datetime.now().strftime("%Y%m%d%H%M%S%f")

    def __str__(self) -> str:
        '''Return the string representation of the roll.'''
        #Every roll must have at lease 1 die and a number of sides 
        self.rollstring = f'Roll {self.pool} d{self.d}.'

        #Next, add modifiers
        if self.threshold > 0:
            self.rollstring += f' Success threshold {self.threshold}.'
        if self.explode > 0:
            self.rollstring += f' Explode {self.explode} or higher.'
        if self.subtractOnes:
            self.rollstring += f' Subtract ones.'
        if self.diceMod > 0:
            self.rollstring += f' Add {self.diceMod} to each die.'
        if self.diceMod < 0:
            self.rollstring += f' Subtract {self.diceMod} from each die.'
        if self.resultMod > 0:
            self.rollstring += f' Add {self.resultMod} to result.'
        if self.resultMod < 0:
            self.rollstring += f' Subtract {self.resultMod} from result.'
        if self.adv != 0:
            if self.adv == 1:
                self.rollstring += ' Roll with advantage.'
            elif self.adv == -1:
                self.rollstring += ' Roll with disadvantage.'

        return self.rollstring

    #We want an option to parse a string notation into a roll as well
    @classmethod
    def _from_notation(cls, notation: str):
        """
        Parse dice notation into components. This will work with standard d20 notation of AdX+B, but also supports following modifiers:
        - !5 - explode 5
        - t5 - success threshold 5
        - s - subtract ones from total success count
        - !5 - explode values of 5 or higher
        - avd or dis - roll with advantage/disadvantage
        Modifiers can be combined in any order. The string MUST have at leaset a 'd' followed by a number of die sides. 
        Adding a + or - modifier to each die rolled is not supported, use initialization from args instead.

        Examples:
        - '8d6!6t5' - 8 dice, explode 6 or higher, success threshold 5
        - 'd20adv' - roll 1 d20 with advantage
        - '2d6+4' - roll 2 d6 and add 4 to result
        """ 
        #   We don't want to deal with 'adv' and 'dis' because 
        #   'd' is reserved for dice sides, so replace them
        notation = notation.lower().replace('adv', 'u').replace('dis', 'z')
        #   Read the input string and turn it into a list
        storestr = '0'
        arglist = []
        if notation[0] == 'd':
            arglist.append(1)                       #   needed to always have a number of dice at the start and account for short notation like 'd20'
        for char in notation:    
            if char.isdigit():
                storestr += char                    #   if char is a number, append to storestr
            else:
                if storestr != '0':
                    arglist.append(int(storestr))   #   if storestr is not empty, conver it to int and append to arglist
                arglist.append(char)                #   append char to arglist
                storestr = '0'                      #   reset storestr
        if storestr != '0':
            arglist.append(int(storestr))
        #print(arglist)

        #   Now that we have a list of strings and ints, figure out 
        #   which list item is which roll attribute and assign variables
        n: int = 0
        d: int = 0
        t: int = 0
        e: int = 0
        adv: int = 0
        rmod: int = 0
        s: bool = False
        for i, char in enumerate(arglist):
            match char:
                case 'd':                       
                    d = arglist[i+1]            #If we have a d, then the previous list item is the number of dice
                    n = arglist[i-1]            #and the next list item is the number of sides
                case 't':                       
                    t = arglist[i+1]
                case '!':
                    e = arglist[i+1]
                case '+':
                    rmod = arglist[i+1]
                case '-':
                    rmod = -arglist[i+1]      
                case 'u':
                    adv = 1
                case 'z':
                    adv = -1
                case 's':
                    s = True


        return cls(n, d, threshold=t, explode=e, subtractOnes=s, resultMod=rmod, adv=adv)
"""
DiceTower class for executing dice rolls.
This class stores settings and executes dice rolls.
Pass a Roll object or init to this class to roll the dice.
"""

from .roll import Roll
import random as rnd
from typing import List, Dict, Tuple, Set, Optional, TypeVar, Union
import csv
import os
import datetime


class DiceTower:
    """A class that handles the execution of dice rolls."""




    def __init__(self, seed:Optional[int]=None, log:Optional[bool]=False) -> None:
        
        """
        Attributes:
            seed: optional int to set a rng instance for reproduceability.
            log: optional bool to enable logging of all rolls in log.txt
        """
        self.seed = seed
        self.rng = rnd.Random(seed)
        self.LastRoll = Roll(1, 20, name='Default Roll')
        self.LastRollResult = 0
        self.LastRollDetailed = []
        self.LoadedRolls = {}
        #self.RollHistory = []
        self.log = log

    def __str__(self) -> str:
        return f'Dice Tower with seed of {self.seed}'

    def _logroll(self):
        if self.log:
            with open('log.txt', 'a') as log:
                logstring = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3] + '. Name: ' + self.LastRoll.name + '\n' + str(self.LastRoll) + ' Result: ' + str(self.LastRollResult) + ', all dice rolled: ' + str(self.LastRollDetailed) + '\n')
                logstring = logstring.replace('Roll', 'Rolled').replace('. Rolled with', ', with')
                log.write(logstring)

    def _counthits(self, result:list [int], threshold:int, subtractOnes:bool=False) -> int:
        s = 0
        for i in result:
            if i >= threshold:
                s = s+1
            elif i == 1 and subtractOnes:
                s = s-1
        return s if s>0 else 0

    def _straightroll(self, sides:int, count:int=1, explode:int=0, dmod:int=0) -> list[int]:
        """
        Roll a number of n-sided dice and return the roll result as a list of ints.

        Arguments:
            sides           - required, int:            number of die sides (e.g. 6 for a common board game die)
            count           - optional, default 1:      the number of dice to roll at a time 
            explode         - optional, default 0:      if set higher than 0, keeps roll result and rolls again if result > threshold 
        """
        if sides < 1 or count < 1:
            raise ValueError("Number of die sides and dice pool count must be positive integers")
        if explode > sides or explode  < 0:
            raise ValueError("Explode value cannot be negative or greater than number of sides")


        rolls = []
        
        while count > 0:
            r = self.rng.randint(1, sides) + dmod
            if explode>0 and r>=explode:
                count = count+1
            if r > sides:
                rolls.append(sides)
            elif r < 1:
                rolls.append(1)
            else:
                rolls.append(r)
            count = count-1
        #print(rolls)
        return rolls
        
    def roll(self, roll:Roll):
        '''
        Execute a dice roll. Pass a Roll object to this method to execute the roll with the settings specified in the Roll object.
        '''
        # Create a last roll from the roll object
        self.LastRoll = Roll(
            pool=roll.pool,
            d=roll.d,
            threshold=roll.threshold,
            explode=roll.explode,
            subtractOnes=roll.subtractOnes,
            diceMod=roll.diceMod,
            resultMod=roll.resultMod,
            adv=roll.adv,
            name=roll.name
        )


        #We will handle the advantage-disadvantage logic here with a case statement
        match roll.adv:
            case 0:
                result = self._straightroll(roll.d, roll.pool, roll.explode, roll.diceMod)
                self.LastRollDetailed = result
                if roll.threshold > 0:
                    self.LastRollResult = self._counthits(result, roll.threshold, roll.subtractOnes)+roll.resultMod
                    self._logroll()
                    return self._counthits(result, roll.threshold, roll.subtractOnes)+roll.resultMod
                else:
                    self.LastRollResult = sum(result)+roll.resultMod
                    self._logroll()
                    return sum(result)+roll.resultMod
            case 1: #advantage
                result1 = self._straightroll(roll.d, roll.pool, roll.explode, roll.diceMod)
                result2 = self._straightroll(roll.d, roll.pool, roll.explode, roll.diceMod)
                #save BOTH rolls to logging
                self.LastRollDetailed = [result1, result2]
                if roll.threshold > 0:
                    self.LastRollResult = max(
                        self._counthits(result1, roll.threshold, roll.subtractOnes)+roll.resultMod,
                        self._counthits(result2, roll.threshold, roll.subtractOnes)+roll.resultMod)
                    self._logroll()
                    return max(
                        self._counthits(result1, roll.threshold, roll.subtractOnes)+roll.resultMod,
                        self._counthits(result2, roll.threshold, roll.subtractOnes)+roll.resultMod) 
                else:
                    #save max total for logging
                    self.LastRollResult = max(
                        sum(result1)+roll.resultMod, 
                        sum(result2)+roll.resultMod)
                    self._logroll()
                    return max(
                        sum(result1)+roll.resultMod, 
                        sum(result2)+roll.resultMod)
            case -1: #disadvantage
                result1 = self._straightroll(roll.d, roll.pool, roll.explode, roll.diceMod)
                result2 = self._straightroll(roll.d, roll.pool, roll.explode, roll.diceMod)
                #Save both rolls to logging
                self.LastRollDetailed = [result1, result2]
                if roll.threshold > 0:
                    self.LastRollResult = min(
                        self._counthits(result1, roll.threshold, roll.subtractOnes)+roll.resultMod,
                        self._counthits(result2, roll.threshold, roll.subtractOnes)+roll.resultMod) 
                    self._logroll()
                    return min(
                        self._counthits(result1, roll.threshold, roll.subtractOnes)+roll.resultMod,
                        self._counthits(result2, roll.threshold, roll.subtractOnes)+roll.resultMod) 
                else:
                    #save min total for logging
                    self.LastRollResult = min(
                        sum(result1)+roll.resultMod, 
                        sum(result2)+roll.resultMod)
                    self._logroll()
                    return min(
                        sum(result1)+roll.resultMod, 
                        sum(result2)+roll.resultMod)
        
    def reroll(self):
        '''
        Executes the last roll again.
        '''
        return self.roll(self.LastRoll)

    def save_last(self, name:str=''):
        '''
        Saves the last roll to the list of saved rolls.

        Args:
        - name (str) optional: name to override the roll's existing name
        '''
        if name != '':
            self.LastRoll.name = name
        self.LoadedRolls[self.LastRoll.name] = self.LastRoll
    
    def save(self, roll:Roll, name:str=''):
        '''
        Pass a Roll object to this method to save the roll to the list of saved rolls.
        Args:
        - Roll object
        - name (str) optional: name to override the roll's existing name
        '''
        if name != '':
            roll.name = name
        self.LoadedRolls[roll.name] = roll

    def to_csv(self, path:str='saved_rolls.csv'):
        '''
        Save the list of saved rolls to a csv file. Takes a path string as optional argument, default is 'saved_rolls.csv. Will overwrite existing file.
        '''
        csvdict = self.LoadedRolls
        for name, roll in csvdict.items():
            roll.name = name
            #print(f'Roll name is {name} /n Roll is {roll}')

        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Roll_Name', 'Sides', 'Number_of_Dice', 'Check_Threshold', 'Explode_Value', 'Subtract_Ones', 'Dice_Modifier', 'Result_Modifier', 'Advantage(-1/0/1)'])
            for name, roll in csvdict.items():
                row = [roll.name,roll.d,roll.pool,roll.threshold,roll.explode,roll.subtractOnes,roll.diceMod,roll.resultMod, roll.adv]
                writer.writerow(row)
    
    def from_loaded(self):
        '''
        Print the list of saved rolls and ask the user to select one by index. Returns the selected roll result.
        ''' 
        for i, roll in enumerate(self.LoadedRolls.items()):
            print(f'{i}: {roll[1].name} - {roll[1]}')        
        while True:
            try:
                selection = int(input('Select a roll: '))
                break
            except ValueError:
                print('Please enter a number from the list.')
        roll = self.LoadedRolls[list(self.LoadedRolls.keys())[selection]]
        self.LastRoll = roll        
        self.LastRollResult = self.roll(roll)
        return self.LastRollResult            

            
            
    def from_csv(self, path:str='saved_rolls.csv'):
        '''
        Load the list of saved rolls from a csv file. Takes a path string as optional argument, default is 'saved_rolls.csv'.
        Raises FileNotFoundError if the specified file does not exist.
        '''
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file '{path}' does not exist")
            
        with open(path, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)  # skip the headers
            self.LoadedRolls = {}
            for row in reader:
                readroll = Roll(int(row[1]), int(row[2]), threshold=int(row[3]), explode=int(row[4]), subtractOnes=bool(row[5]), diceMod=int(row[6]), resultMod=int(row[7]), adv=int(row[8]))
                self.LoadedRolls[str(row[0])] = readroll






#       logging
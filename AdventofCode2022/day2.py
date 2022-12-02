import sys
sys.path.append('.')
import aoc
import math
from enum import Enum

data_rows = aoc.get_input(2, sample=False, index=0).splitlines()

class Symbol(Enum):
    ROCK = 0,
    PAPER = 1,
    SCISSORS = 2
class Outcome(Enum):
    LOSS = 0,
    DRAW = 1,
    WIN = 2

symbol_map = {"A": Symbol.ROCK, "B": Symbol.PAPER, "C": Symbol.SCISSORS, "X": Symbol.ROCK, "Y": Symbol.PAPER, "Z": Symbol.SCISSORS}
outcome_map = {"X": Outcome.LOSS, "Y": Outcome.DRAW, "Z": Outcome.WIN}
symbol_score_map = {Symbol.ROCK: 1, Symbol.PAPER: 2, Symbol.SCISSORS: 3}
outcome_score_map = {Outcome.LOSS: 0, Outcome.DRAW: 3, Outcome.WIN: 6}

def get_outcome(opp_symbol: Symbol, my_symbol: Symbol) -> Outcome:
    if opp_symbol == my_symbol:
        return Outcome.DRAW
    if (opp_symbol == Symbol.ROCK and my_symbol == Symbol.SCISSORS) or \
       (opp_symbol == Symbol.PAPER and my_symbol == Symbol.ROCK) or \
       (opp_symbol == Symbol.SCISSORS and my_symbol == Symbol.PAPER):
        return Outcome.LOSS
    if (opp_symbol == Symbol.ROCK and my_symbol == Symbol.PAPER) or \
       (opp_symbol == Symbol.PAPER and my_symbol == Symbol.SCISSORS) or \
       (opp_symbol == Symbol.SCISSORS and my_symbol == Symbol.ROCK):
        return Outcome.WIN


def score_row(row: str): 
    chars = row.split()
    opp_symbol = symbol_map[chars[0]]
    my_symbol = symbol_map[chars[1]]
    symbol_score = symbol_score_map[my_symbol]
    outcome = get_outcome(opp_symbol, my_symbol)
    outcome_score = outcome_score_map[outcome]
    print(f"{row}: {opp_symbol.name},{my_symbol.name} -> {outcome.name} | symbol: {symbol_score}, outcome {outcome_score}")
    return symbol_score + outcome_score

def part1():
    total_score = 0
    for row in data_rows:
        total_score += score_row(row)
    print(total_score)
# part1()


def get_move2(opp_symbol: Symbol, outcome: Outcome) -> Symbol:
    if outcome == Outcome.DRAW:
        return opp_symbol
    if (opp_symbol == Symbol.ROCK and outcome == Outcome.WIN) or \
       (opp_symbol == Symbol.SCISSORS and outcome == Outcome.LOSS):
        return Symbol.PAPER
    if (opp_symbol == Symbol.SCISSORS and outcome == Outcome.WIN) or \
       (opp_symbol == Symbol.PAPER and outcome == Outcome.LOSS):
        return Symbol.ROCK
    if (opp_symbol == Symbol.PAPER and outcome == Outcome.WIN) or \
       (opp_symbol == Symbol.ROCK and outcome == Outcome.LOSS):
        return Symbol.SCISSORS

def score_row2(row: str): 
    chars = row.split()
    opp_symbol = symbol_map[chars[0]]
    outcome = outcome_map[chars[1]]
    my_symbol = get_move2(opp_symbol, outcome)
    symbol_score = symbol_score_map[my_symbol]
    outcome_score = outcome_score_map[outcome]
    # print(f"{row}: {opp_symbol.name},{outcome.name} -> {my_symbol.name} | symbol: {symbol_score}, outcome {outcome_score}")
    return symbol_score + outcome_score

def part2():
    total_score = 0
    for row in data_rows:
        total_score += score_row2(row)
    print(total_score)
part2()



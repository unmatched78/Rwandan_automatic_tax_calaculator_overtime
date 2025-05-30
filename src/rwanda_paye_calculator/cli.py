# src/rwanda_paye_calculator/cli.py
import argparse
from .calculator import PAYECalculator
from .deductions import FixedDeduction, PercentageDeduction

def parse_deductions(args):
    deductions = []
    for fd in args.fixed or []:
        deductions.append(FixedDeduction(fd))
    for pd in args.percent or []:
        deductions.append(PercentageDeduction(pd/100))
    return deductions

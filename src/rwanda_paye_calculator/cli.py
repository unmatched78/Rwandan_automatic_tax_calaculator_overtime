# src/rwanda_paye_calculator/cli.py
import argparse
from .calculator import PAYECalculator
from .deductions import FixedDeduction, PercentageDeduction
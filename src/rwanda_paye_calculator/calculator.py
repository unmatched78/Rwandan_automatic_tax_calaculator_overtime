# src/rwanda_paye_calculator/calculator.py
import abc
from typing import List, Dict
from .deductions import Deduction

# Default social security rate and tax brackets (monthly)
SOCIAL_SECURITY_RATE = 0.06
TAX_FREE_ALLOWANCE = 60_000

MONTHLY_BRACKETS = [
    (0, 60_000, 0.00),
    (60_000, 100_000, 0.10),
    (100_000, 200_000, 0.20),
    (200_000, float('inf'), 0.30),
]

ANNUAL_BRACKETS = [(low*12, high*12 if high != float('inf') else float('inf'), rate)
                   for (low, high, rate) in MONTHLY_BRACKETS]
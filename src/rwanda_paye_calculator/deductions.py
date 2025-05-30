# src/rwanda_paye_calculator/deductions.py
from abc import ABC, abstractmethod

class Deduction(ABC):
    @abstractmethod
    def amount(self, gross: float) -> float:
        """Return deduction amount based on gross salary."""
        pass

class FixedDeduction(Deduction):
    def __init__(self, value: float):
        self.value = value

    def amount(self, gross: float) -> float:
        return self.value

class PercentageDeduction(Deduction):
    def __init__(self, rate: float):
        self.rate = rate

    def amount(self, gross: float) -> float:
        return gross * self.rate
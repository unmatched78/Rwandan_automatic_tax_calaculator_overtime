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

class PAYECalculator:
    def __init__(self, gross: float, mode: str = 'monthly', custom_deductions: List[Deduction] = None):
        """
        mode: 'monthly' or 'annual'
        custom_deductions: list of Deduction instances to subtract before tax
        """
        self.gross = gross
        self.mode = mode
        self.deductions = custom_deductions or []

    def _apply_social_security(self, amount: float) -> float:
        return amount * SOCIAL_SECURITY_RATE

    def _compute_taxable(self, gross: float, ssc: float) -> float:
        taxable = gross - ssc - TAX_FREE_ALLOWANCE * (12 if self.mode=='annual' else 1)
        return max(0.0, taxable)

    def _compute_tax(self, taxable: float) -> float:
        brackets = ANNUAL_BRACKETS if self.mode=='annual' else MONTHLY_BRACKETS
        remaining = taxable
        total_tax = 0.0
        for low, high, rate in brackets:
            if remaining <= 0:
                break
            band = max(0, min(remaining, high - low))
            total_tax += band * rate
            remaining -= band
        return total_tax

    def calculate(self) -> Dict[str, float]:
        # 1. Social Security
        ssc = self._apply_social_security(self.gross)
        # 2. Custom deductions
        custom_total = sum(d.amount(self.gross) for d in self.deductions)
        # 3. Taxable income
        taxable = self._compute_taxable(self.gross, ssc) - custom_total
        taxable = max(0.0, taxable)
        # 4. PAYE
        paye = self._compute_tax(taxable)
        net = self.gross - ssc - paye - custom_total
        return {
            'gross': self.gross,
            'social_security': round(ssc,2),
            'custom_deductions': round(custom_total,2),
            'taxable_income': round(taxable,2),
            'paye': round(paye,2),
            'net_pay': round(net,2),
        }

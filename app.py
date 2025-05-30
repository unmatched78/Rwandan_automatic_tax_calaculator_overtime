from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TaxBracket:
    lower: float    # inclusive lower bound
    upper: float    # inclusive upper bound (use float('inf') for no cap)
    rate: float     # e.g. 0.10 for 10%

# Define Rwanda PAYE brackets (monthly)
BRACKETS: List[TaxBracket] = [
    TaxBracket(0, 60_000, 0.00),
    TaxBracket(60_000, 100_000, 0.10),
    TaxBracket(100_000, 200_000, 0.20),
    TaxBracket(200_000, float('inf'), 0.30),
]

def calculate_paye(gross_salary: float) -> dict:
    """
    Calculate PAYE breakdown for a given gross monthly salary in RWF.
    Returns a dict with breakdown of SSC, taxable income, tax per bracket, and total PAYE.
    """
    # 1. Employee social security contribution (6%)
    ssc = 0.06 * gross_salary

    # 2. Taxable income after allowance
    taxable = max(0.0, gross_salary - ssc - 60_000)

    # 3. Calculate tax per bracket
    remaining = taxable
    tax_details: List[Tuple[Tuple[float, float], float, float]] = []
    total_tax = 0.0

    for br in BRACKETS:
        if remaining <= 0:
            break
        # Determine income in this bracket
        # Amount over br.lower up to br.upper
        lower, upper = br.lower, br.upper
        # Tax applies only above the lower threshold
        taxable_in_bracket = max(0, min(remaining, upper - lower))
        tax_for_bracket = taxable_in_bracket * br.rate
        tax_details.append(((lower, upper), taxable_in_bracket, tax_for_bracket))
        total_tax += tax_for_bracket
        remaining -= taxable_in_bracket

    return {
        "gross_salary": gross_salary,
        "social_security (6%)": round(ssc, 2),
        "taxable_income": round(taxable, 2),
        "tax_breakdown": [
            {
                "bracket": f"{int(lb)}–{'∞' if ub==float('inf') else int(ub)}",
                "taxable_amount": round(amount, 2),
                "rate": f"{int(rate*100)}%",
                "tax": round(tax, 2),
            }
            for (lb, ub), amount, tax in tax_details for rate in [next(b.rate for b in BRACKETS if b.lower==lb)]
        ],
        "total_paye": round(total_tax, 2),
        "net_salary": round(gross_salary - ssc - total_tax, 2),
    }

# Example usage
if __name__ == "__main__":
    for salary in [100_000, 150_000, 300_000]:
        result = calculate_paye(salary)
        print(f"\nGross salary: RWF {salary}")
        print(f" – Social Security (6%): RWF {result['social_security (6%)']}")
        print(f" – Taxable Income: RWF {result['taxable_income']}")
        for b in result["tax_breakdown"]:
            print(f"   • {b['bracket']} @ {b['rate']}: RWF {b['taxable_amount']} → Tax RWF {b['tax']}")
        print(f" – Total PAYE: RWF {result['total_paye']}")
        print(f" – Net Salary: RWF {result['net_salary']}")

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

##################
def main():
    parser = argparse.ArgumentParser(description='Rwanda PAYE Calculator')
    parser.add_argument('--gross', type=float, required=True, help='Gross salary')
    parser.add_argument('--mode', choices=['monthly','annual'], default='monthly')
    parser.add_argument('--fixed', nargs='*', type=float, help='Fixed deductions amounts')
    parser.add_argument('--percent', nargs='*', type=float, help='Percentage deductions (e.g. 5 for 5%)')
    args = parser.parse_args()

    deductions = parse_deductions(args)
    calc = PAYECalculator(args.gross, mode=args.mode, custom_deductions=deductions)
    result = calc.calculate()
    for k, v in result.items():
        print(f"{k}: RWF {v}")
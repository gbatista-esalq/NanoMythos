"""
TDD Pym Quântico Test Suite for Lobster Challenge Solver.
Ensures perfect decryption of anti-bot challenge puzzles with complex obfuscation.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scratch.lobster_solver import auto_solve_challenge

def test_auto_solve_addition():
    challenge = "ThIs] LoOo-bS tEr^ SwImS[ aT Tw/eNn-Ty ThReE} CeNtI/mEteRs\\ PeR Um SeCoNd| AnD- AnO tHeR~ InCrEaSeS^ SpEeD{ By SeVeN< , WhAt] Is- ThE ToTaL~ SpEeD?"
    ans = auto_solve_challenge(challenge)
    assert ans == "30.00"

def test_auto_solve_multiplication():
    challenge = "Cl]Aw F^oRcE Is ThIrTy TwO NooTtOnS / MuLtIiPllIiEd By FoUr Lo.bSt- Errs ~ WhAtS ToTaL F^oRcE?"
    ans = auto_solve_challenge(challenge)
    assert ans == "128.00"

def test_auto_solve_subtraction():
    challenge = "velocity is thirty one meters per second, reduce speed by four and then slows down by nine meters"
    ans = auto_solve_challenge(challenge)
    # 31 - 4 - 9 = 18
    assert ans == "18.00"

def test_auto_solve_distractors():
    challenge = "lobster with twenty two claws exerts force of forty five kilograms and slows down by nine"
    ans = auto_solve_challenge(challenge)
    # Distractor 22 (number of claws) is ignored because it's first and there are 3 numbers.
    # The math is forty five (45) reduced by nine (9) -> 36
    assert ans == "36.00"

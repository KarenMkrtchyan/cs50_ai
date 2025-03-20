from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    # Not(And(AKnave, AKnight)),
    # Or(And(AKnight, And(AKnave, AKnight))),
    And(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    And(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(And(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))), And(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave))))),
    Biconditional(BKnave, AKnight),
    Biconditional(BKnight, AKnave),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
A_said_knight = Symbol("A said knight")
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Biconditional(A_said_knight, Or(AKnave, AKnight)), # potentially too much logic used to write this line. a knight would never say I am a knave bc thats a lie, a knave would never say I am a knave bc thats the truth

    Biconditional(BKnight, A_said_knight),
    Biconditional(BKnave, Not(A_said_knight)),

    Biconditional(BKnight, CKnave),
    Biconditional(BKnave, CKnight),

    Biconditional(CKnight, AKnight),
    Implication(AKnave, CKnave),


    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

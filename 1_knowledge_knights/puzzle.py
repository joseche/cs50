from logic import Symbol, And, Or, Not, model_check, Implication

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(And(AKnight, AKnave), And(AKnave, Not(And(AKnight, AKnave))))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(  # a is knight or knave, but not both
        Or(AKnight, AKnave), Not(And(AKnight, AKnave))
    ),
    And(  # b is knight or knave but not both
        Or(BKnight, BKnave), Not(And(BKnight, BKnave))
    ),
    Or(
        And(AKnight, And(AKnave, BKnave)),
        And(AKnave, Not(And(AKnave, BKnave))),
    ),
    And(AKnave, Not(BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(  # a is knight or knave, but not both
        Or(AKnight, AKnave), Not(And(AKnight, AKnave))
    ),
    And(  # b is knight or knave but not both
        Or(BKnight, BKnave), Not(And(BKnight, BKnave))
    ),
    Or(
        And(
            AKnight,  # if he is a knight
            Or(  # he says, they are the same kind, so they are either knights or...
                And(AKnight, BKnight), And(AKnave, BKnave)
            ),
        ),
        And(
            AKnave,  # if he is a knave
            Not(
                Or(  # he says, they are the same kind, so they are either knights or...
                    And(AKnight, BKnight), And(AKnave, BKnave)
                )
            ),  # or they are knaves,
        ),
    ),
    And(BKnight, Not(AKnight)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(  # a is knight or knave, but not both
        Or(AKnight, AKnave), Not(And(AKnight, AKnave))
    ),
    And(  # b is knight or knave but not both
        Or(BKnight, BKnave), Not(And(BKnight, BKnave))
    ),
    And(  # c is knight or knave but not both
        Or(CKnight, CKnave), Not(And(CKnight, CKnave))
    ),
    Implication(AKnight, Or(AKnave, AKnight)),  # not adding anything,,,
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),
    Implication(
        BKnight,
        And(
            Not(Implication(AKnight, Or(AKnave, AKnight))),
            Implication(AKnight, Or(AKnave, AKnight)),
        ),
    ),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
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

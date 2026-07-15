
from parsing.ast import Fact, And, Or, Xor, Not

class ExpressionParser:

    def parse(self, expression):

        # NOT (priorité la plus haute)
        if expression.startswith("!"):
            return Not(
                self.parse(expression[1:])
            )

        # AND
        if "+" in expression:
            left, right = expression.split("+", 1)
            return And(
                self.parse(left),
                self.parse(right)
            )

        # OR
        if "|" in expression:
            left, right = expression.split("|", 1)
            return Or(
                self.parse(left),
                self.parse(right)
            )

        # XOR
        if "^" in expression:
            left, right = expression.split("^", 1)
            return Xor(
                self.parse(left),
                self.parse(right)
            )

        return Fact(expression)
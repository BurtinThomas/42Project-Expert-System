from parsing.ast import Fact, And, Or, Xor, Not


class ExpressionParser:

    def find_operator(self, expression, operator):
        depth = 0
        for i, c in enumerate(expression):
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == operator and depth == 0:
                return i
        return -1

    def remove_parentheses(self, expression):
        while (
            expression.startswith("(")
            and expression.endswith(")")
        ):
            depth = 0
            valid = True
            for i, c in enumerate(expression):
                if c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                if depth == 0 and i != len(expression) - 1:
                    valid = False
                    break
            if valid:
                expression = expression[1:-1]
            else:
                break
        return expression

    def parse(self, expression):
        expression = self.remove_parentheses(expression)

        # XOR (priorité la plus faible)
        i = self.find_operator(expression, "^")
        if i != -1:
            return Xor(
                self.parse(expression[:i]),
                self.parse(expression[i + 1:])
            )
        # OR
        i = self.find_operator(expression, "|")
        if i != -1:
            return Or(
                self.parse(expression[:i]),
                self.parse(expression[i + 1:])
            )
        # AND
        i = self.find_operator(expression, "+")
        if i != -1:
            return And(
                self.parse(expression[:i]),
                self.parse(expression[i + 1:])
            )
        # NOT (priorité la plus haute)
        if expression.startswith("!"):
            return Not(
                self.parse(expression[1:])
            )
        return Fact(expression)
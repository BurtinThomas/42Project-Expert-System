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


    def check_parentheses(self, expression):
        depth = 0
        for c in expression:
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            if depth < 0:
                raise SyntaxError("Invalid parentheses")
        if depth != 0:
            raise SyntaxError("Invalid parentheses")


    def check_operators(self, expression):
        operators = "+|^"
        for i, c in enumerate(expression):
            if i == 0 and c in operators:
                raise SyntaxError("Operator without left operand")
            if i == len(expression) - 1 and c in operators:
                raise SyntaxError("Operator without right operand")
            if (
                i < len(expression) - 1
                and c in operators
                and expression[i + 1] in operators
            ):
                raise SyntaxError("Two operators together")


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
        self.check_parentheses(expression)
        self.check_operators(expression)
        expression = self.remove_parentheses(expression)
        i = self.find_operator(expression, "^")
        if i != -1:
            left = expression[:i]
            right = expression[i + 1:]
            if not left or not right:
                raise SyntaxError("Missing operand")
            return Xor(
                self.parse(left),
                self.parse(right)
            )
        # OR
        i = self.find_operator(expression, "|")
        if i != -1:
            left = expression[:i]
            right = expression[i + 1:]
            if not left or not right:
                raise SyntaxError("Missing operand")
            return Or(
                self.parse(left),
                self.parse(right)
            )
        # AND
        i = self.find_operator(expression, "+")
        if i != -1:
            left = expression[:i]
            right = expression[i + 1:]
            if not left or not right:
                raise SyntaxError("Missing operand")
            return And(
                self.parse(left),
                self.parse(right)
            )
        # NOT
        if expression.startswith("!"):
            if len(expression) == 1:
                raise SyntaxError("Missing operand after !")
            return Not(
                self.parse(expression[1:])
            )
        # Fact
        if len(expression) != 1 or not expression.isupper():
            raise SyntaxError(f"Invalid fact: {expression}")
        return Fact(expression)
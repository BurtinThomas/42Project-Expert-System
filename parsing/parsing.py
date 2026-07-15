
from parsing.expression_parser import ExpressionParser

class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Parser:
    def __init__(self, filename):
        self.rules = []
        self.facts = set()
        self.queries = []

        self.expression_parser = ExpressionParser()
        self.load(filename)


    def load(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.split('#')[0]
                line = line.strip()
                line = line.replace(" ", "")
                if not line:
                    continue
                if line.startswith('='):
                    self.facts.update(line[1:])
                elif line.startswith('?'):
                    self.queries.extend(line[1:])
                elif '=>' in line:
                    left, right = line.split('=>')
                    left = self.expression_parser.parse(left)
                    right = self.expression_parser.parse(right)
                    self.rules.append(
                        Rule(left, right)
                    )
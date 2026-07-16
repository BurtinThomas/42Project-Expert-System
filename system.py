from parsing.ast import Fact, And, Or, Xor, Not


class ExpertSystem:

    def __init__(self, rules, facts):
        self.rules = rules
        self.facts = set(facts)


    def evaluate(self, node, visiting):
        # FACT
        if isinstance(node, Fact):
            return self.prove(node.name, visiting)
        # NOT
        if isinstance(node, Not):
            return not self.evaluate(node.child, visiting)
        # AND
        if isinstance(node, And):
            left = self.evaluate(node.left, visiting)
            right = self.evaluate(node.right, visiting)
            return left and right
        # OR
        if isinstance(node, Or):
            left = self.evaluate(node.left, visiting)
            right = self.evaluate(node.right, visiting)
            return left or right
        # XOR
        if isinstance(node, Xor):
            left = self.evaluate(node.left, visiting)
            right = self.evaluate(node.right, visiting)
            return left != right
        return False


    def prove(self, query, visiting=None):
        if visiting is None:
            visiting = set()
        if query in self.facts:
            return True
        if query in visiting:
            return False
        visiting.add(query)
        for rule in self.rules:
            if isinstance(rule.right, Fact) and rule.right.name == query:
                if self.evaluate(rule.left, visiting):
                    self.facts.add(query)
                    visiting.remove(query)
                    return True
        visiting.remove(query)
        return False
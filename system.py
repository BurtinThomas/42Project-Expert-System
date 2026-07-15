
class ExpertSystem:

    def __init__(self, rules, facts):
        self.rules = rules
        self.facts = facts

    def prove(self, query):
        # Est-ce déjà un fait connu ?
        if query in self.facts:
            return True
        # Chercher une règle qui conclut ce fait
        for rule in self.rules:
            if rule.right.name == query:
                return self.evaluate(rule.left)
        return False
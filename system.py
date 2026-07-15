
from parsing.ast import Fact, And, Or, Xor, Not

class ExpertSystem:

    def __init__(self, rules, facts):
        self.rules = rules
        self.facts = facts


    def evaluate(self, node):
        print("\n--------------------------------")
        print(f"Node reçu : {node}")
        print(f"Type      : {type(node)}")

        # FACT
        if isinstance(node, Fact):
            result = node.name in self.facts
            print(f"Fact rencontré : {node.name}")
            print(f"Est dans les faits ? {result}")
            return result

        # NOT
        if isinstance(node, Not):
            print("Opérateur NOT")
            print(f"On évalue : {node.child}")
            child = self.evaluate(node.child)
            result = not child
            print(f"NOT {child} = {result}")
            return result

        # AND
        if isinstance(node, And):
            print("Opérateur AND")
            print("Évaluation du côté gauche")
            left = self.evaluate(node.left)
            print("Évaluation du côté droit")
            right = self.evaluate(node.right)
            result = left and right
            print(f"{left} AND {right} = {result}")
            return result

        # OR
        if isinstance(node, Or):
            print("Opérateur OR")
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            result = left or right
            print(f"{left} OR {right} = {result}")
            return result

        # XOR
        if isinstance(node, Xor):
            print("Opérateur XOR")
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            result = left != right
            print(f"{left} XOR {right} = {result}")
            return result
        print("Type inconnu !")
        return False
        

    def prove(self, query):
        # Est-ce déjà un fait connu ?
        if query in self.facts:
            return True
        # Chercher une règle qui conclut ce fait
        for rule in self.rules:
            if rule.right.name == query:
                return self.evaluate(rule.left)
        return False
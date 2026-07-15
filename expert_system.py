import os
import sys
from parsing.parsing import Parser
from expert_system import ExpertSystem


def print_ast(node, level=0):
    """
    Affiche récursivement l'arbre AST.
    """
    indent = "  " * level
    print(f"{indent}{type(node).__name__}: {node}")
    # Pour And, Or, Xor
    if hasattr(node, "left") and hasattr(node, "right"):
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)
    # Pour Not
    elif hasattr(node, "child"):
        print_ast(node.child, level + 1)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <input_file>")
        return
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return

    parser = Parser(filename)

    print("\n=== RULES ===")
    for rule in parser.rules:
        print("\nRule:")
        
        print("Condition:")
        print_ast(rule.left)

        print("Conclusion:")
        print_ast(rule.right)

    print("\n=== FACTS ===")
    print(parser.facts)

    print("\n=== QUERIES ===")
    print(parser.queries)

    system = ExpertSystem(
        parser.rules,
        parser.facts
    )

    for query in parser.queries:
        result = system.prove(query)
        print(f"{query}: {result}")

if __name__ == "__main__":
    main()
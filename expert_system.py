import os
import sys
from parsing.parsing import Parser
from system import ExpertSystem


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <input_file>")
        return
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return

    parser = Parser(filename)

    system = ExpertSystem(
        parser.rules,
        parser.facts
    )

    for query in parser.queries:
        result = system.prove(query)
        print(f"{query}: {result}")

if __name__ == "__main__":
    main()
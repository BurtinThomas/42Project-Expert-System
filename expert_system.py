import os
import sys
from parsing.parsing import Parser
from system import ExpertSystem


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python expert_system.py <filename>")
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        if os.path.getsize("input/file.txt") == 0:
            raise ValueError("File is empty")
        parser = Parser(filename)
        system = ExpertSystem(
            parser.rules,
            parser.facts
        )
        for query in parser.queries:
            result = system.prove(query)
            print(f"{query}: {result}")
    except Exception as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main()
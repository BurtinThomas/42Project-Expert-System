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

        self.facts_found = False
        self.queries_found = False

        self.load(filename)


    def load(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.split('#')[0]
                line = line.strip()
                line = "".join(line.split())
                if not line:
                    continue
                if line.startswith('='):
                    if self.facts_found:
                        raise SyntaxError("Multiple facts declarations")
                    self.facts_found = True
                    self.parse_facts(line)
                elif line.startswith('?'):
                    if self.queries_found:
                        raise SyntaxError("Multiple query declarations")
                    self.queries_found = True
                    self.parse_queries(line)
                elif '=>' in line:
                    self.parse_rule(line)
                else:
                    raise SyntaxError(f"Invalid line: {line}")
        if not self.facts_found:
            raise SyntaxError("Missing facts declaration")
        if not self.queries_found:
            raise SyntaxError("Missing queries declaration")
        self.check_rule_contradictions()


    def parse_facts(self, line):
        facts = line[1:]
        if not facts:
            return
        for fact in facts:
            if not fact.isupper() or len(fact) != 1:
                raise SyntaxError(f"Invalid fact: {fact}")
            if fact.lower() in self.facts:
                raise SyntaxError(f"Contradiction in facts: {fact} and !{fact}")
            self.facts.add(fact)


    def parse_queries(self, line):
        queries = line[1:]
        if not queries:
            raise SyntaxError("Empty query declaration")
        for query in queries:
            if not query.isupper() or len(query) != 1:
                raise SyntaxError(f"Invalid query: {query}")
            self.queries.append(query)


    def parse_rule(self, line):
        if line.count("=>") != 1:
            raise SyntaxError("Invalid rule implication")
        left, right = line.split("=>")
        if not left or not right:
            raise SyntaxError("Missing rule operand")
        left = self.expression_parser.parse(left)
        conclusions = right.split("+")
        parsed_conclusions = []
        for conclusion in conclusions:
            if not conclusion:
                raise SyntaxError("Empty conclusion")
            right_expression = self.expression_parser.parse(conclusion)
            parsed_conclusions.append(right_expression)
            self.rules.append(Rule(left, right_expression))
        self.check_local_contradiction(parsed_conclusions)


    def check_local_contradiction(self, conclusions):
        positives = set()
        negatives = set()
        for conclusion in conclusions:
            value = str(conclusion)
            if value.startswith("!"):
                fact = value[1:]
                negatives.add(fact)
            else:
                positives.add(value)
        contradiction = positives.intersection(negatives)
        if contradiction:
            fact = contradiction.pop()
            raise SyntaxError(f"Contradiction in rule conclusion: {fact} and !{fact}")


    def check_rule_contradictions(self):
        conclusions = {}
        for rule in self.rules:
            value = str(rule.right)
            if value.startswith("!"):
                fact = value[1:]
                if fact in conclusions and conclusions[fact] == "positive":
                    raise SyntaxError(f"Contradiction between rules: {fact} and !{fact}")
                conclusions[fact] = "negative"
            else:
                fact = value
                if fact in conclusions and conclusions[fact] == "negative":
                    raise SyntaxError(f"Contradiction between rules: {fact} and !{fact}")
                conclusions[fact] = "positive"

class Fact:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} + {self.right})"


class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} | {self.right})"


class Xor:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} ^ {self.right})"


class Not:
    def __init__(self, child):
        self.child = child

    def __repr__(self):
        return f"!{self.child}"
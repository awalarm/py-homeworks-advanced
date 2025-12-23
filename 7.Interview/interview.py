import pytest


class Stack:

    def __init__(self):
        self.arr = []

    def is_empty(self):
        return len(self.arr) == 0

    def push(self, value):
        self.arr.append(value)

    def pop(self):
        if self.is_empty():
            return None
        return self.arr.pop()

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.arr[-1]

    def size(self):
        return len(self.arr)


def is_balanced(value):
    stack = Stack()
    for el in value:
        if el == "(" or el == "[" or el == "{":
            stack.push(el)
        elif (
            (el == ")" and stack.peek() == "(")
            or (el == "]" and stack.peek() == "[")
            or (el == "}" and stack.peek() == "{")
        ):
            stack.pop()
        else:
            return "Несбалансированно"

    if stack.is_empty():
        return "Сбалансированно"

    return "Несбалансированно"


@pytest.mark.parametrize(
    "brackets_string", ["(((([{}]))))", "[([])((([[[]]])))]{()}", "{{[()]}}"]
)
def test_balanced_sequences(brackets_string):
    result = is_balanced(brackets_string)
    assert (
        result == "Сбалансированно"
    ), f"Ожидалось 'Сбалансированно' для '{brackets_string}'"


@pytest.mark.parametrize("brackets_string", ["}{}", "{{[(])]}}", "[[{())}]"])
def test_unbalanced_sequences(brackets_string):
    result = is_balanced(brackets_string)
    assert (
        result == "Несбалансированно"
    ), f"Ожидалось 'Несбалансированно' для '{brackets_string}'"

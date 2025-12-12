class FlatIterator:

    def __init__(self, list_of_list):
        self.stack = []
        self._push_iterator(iter(list_of_list))

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            current_iterator = self.stack[-1]

            try:
                item = next(current_iterator)

                if isinstance(item, list):
                    self._push_iterator(iter(item))
                else:
                    return item

            except StopIteration:
                self.stack.pop()
                continue

        raise StopIteration

    def _push_iterator(self, param):
        self.stack.append(param)


def test_1():
    list_of_lists_1 = [["a", "b", "c"], ["d", "e", "f", "h", False], [1, 2, None]]

    for flat_iterator_item, check_item in zip(
        FlatIterator(list_of_lists_1),
        ["a", "b", "c", "d", "e", "f", "h", False, 1, 2, None],
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "h",
        False,
        1,
        2,
        None,
    ]


def test_2():
    list_of_lists_2 = [
        [["a"], ["b", "c"]],
        ["d", "e", [["f"], "h"], False],
        [1, 2, None, [[[[["!"]]]]], []],
    ]

    for flat_iterator_item, check_item in zip(
        FlatIterator(list_of_lists_2),
        ["a", "b", "c", "d", "e", "f", "h", False, 1, 2, None, "!"],
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "h",
        False,
        1,
        2,
        None,
        "!",
    ]


if __name__ == "__main__":
    test_1()
    test_2()

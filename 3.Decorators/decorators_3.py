import types
from datetime import datetime
from functools import wraps


def logger(path):
    count = 0

    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            nonlocal count
            count += 1

            current_time = datetime.now()
            result = old_function(*args, **kwargs)
            with open(path, "a", encoding="utf-8") as f:
                f.write(
                    f"{count}) {current_time} {old_function.__name__} {args}, {kwargs}\n"
                )
            return result

        return new_function

    return __logger


@logger("test1.txt")
def flat_generator(list_of_list):
    for item in list_of_list:
        if isinstance(item, list):
            # yield from flat_generator(item)
            for i in flat_generator(item):
                yield i
        else:
            yield item


def test_4():
    list_of_lists_2 = [
        [["a"], ["b", "c"]],
        ["d", "e", [["f"], "h"], False],
        [1, 2, None, [[[[["!"]]]]], []],
    ]

    for flat_iterator_item, check_item in zip(
        flat_generator(list_of_lists_2),
        ["a", "b", "c", "d", "e", "f", "h", False, 1, 2, None, "!"],
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_2)) == [
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

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == "__main__":
    test_4()

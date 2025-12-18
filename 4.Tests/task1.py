import pytest


# Модифицированные функции (заменили print на return)


def discriminant(a, b, c):
    """
    Функция для нахождения дискриминанта
    """
    return b**2 - 4 * a * c


def solution(a, b, c):
    """
    Функция для нахождения корней квадратного уравнения
    Теперь возвращает результат вместо печати
    """
    D = discriminant(a, b, c)

    if D < 0:
        return "корней нет"
    elif D == 0:
        x = -b / (2 * a)
        return str(x)
    else:
        x1 = (-b + D**0.5) / (2 * a)
        x2 = (-b - D**0.5) / (2 * a)
        return f"{x1} {x2}"


def solve(phrases: list):
    """
    Функция для поиска палиндромов в списке фраз
    """
    result = []
    for phrase in phrases:
        str = phrase.replace(" ", "")
        if str == str[::-1]:
            result.append(phrase)
    return result


# Тесты для функции solution
@pytest.mark.parametrize(
    "a,b,c,expected",
    [(1, 8, 15, "-3.0 -5.0"), (1, -2, 1, "1.0"), (1, 2, 5, "корней нет")],
)
def test_solution(a, b, c, expected):
    """Тестирование решения квадратных уравнений"""
    assert solution(a, b, c) == expected


# Тесты для функции discriminant
@pytest.mark.parametrize(
    "a,b,c,expected", [(1, 8, 15, 4), (1, -2, 1, 0), (1, 2, 5, -16)]
)
def test_discriminant(a, b, c, expected):
    """Тестирование вычисления дискриминанта"""
    assert discriminant(a, b, c) == expected


# Тесты для функции solve
@pytest.mark.parametrize(
    "phrases,expected",
    [
        (["казак"], ["казак"]),
        (["а роза упала на лапу азора"], ["а роза упала на лапу азора"]),
        (["мадам", "тест", "шалаш"], ["мадам", "шалаш"]),
        (
            ["а роза упала на лапу азора", "не палиндром"],
            ["а роза упала на лапу азора"],
        ),
        ([], []),
        (["привет", "мир", "python"], []),
    ],
)
def test_solve(phrases, expected):
    """Тестирование поиска палиндромов"""
    assert solve(phrases) == expected


if __name__ == "__main__":
    pytest.main()

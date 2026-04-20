# vector_math.py
"""
Модуль для работы с N-мерными математическими векторами.
Реализует класс Vector с поддержкой сложения, умножения и вычисления нормы.
"""

import math
from typing import Union, Tuple


class Vector:
    """
    Иммутабельный (неизменяемый) N-мерный вектор.
    Поддерживает операции сложения, умножения на скаляр и скалярного произведения.
    """

    def __init__(self, *coords: float) -> None:
        """
        Инициализация вектора произвольным количеством координат.

        :param coords: числа с плавающей точкой, задающие компоненты вектора
        """
        # Преобразуем все координаты во float для единообразия
        self._coords = tuple(float(x) for x in coords)

    @property
    def coords(self) -> Tuple[float, ...]:
        """Возвращает кортеж координат вектора (только для чтения)."""
        return self._coords

    def __len__(self) -> int:
        """Возвращает размерность вектора."""
        return len(self._coords)

    def __str__(self) -> str:
        """
        Красивое представление без лишних десятичных нулей.
        Целые числа отображаются как целые.
        """
        parts = []
        for c in self._coords:
            # Для float-чисел проверяем, является ли оно целым
            if c.is_integer():
                parts.append(str(int(c)))
            else:
                # Убираем незначащие нули с помощью :g
                parts.append(f"{c:g}")
        return f"Vector({', '.join(parts)})"

    def __repr__(self) -> str:
        """
        Строковое представление для разработчика.
        Позволяет воссоздать объект.
        """
        return f"Vector{self._coords}"

    def __add__(self, other: "Vector") -> "Vector":
        """
        Покомпонентное сложение двух векторов одинаковой размерности.

        :param other: другой объект Vector
        :return: новый объект Vector
        :raises ValueError: если размерности не совпадают
        :raises TypeError: если other не является Vector
        """
        if not isinstance(other, Vector):
            raise TypeError(f"Сложение возможно только с Vector, получен {type(other)}")
        if len(self) != len(other):
            raise ValueError(
                f"Векторы разной размерности: {len(self)} и {len(other)}"
            )

        new_coords = tuple(a + b for a, b in zip(self._coords, other._coords))
        return Vector(*new_coords)

    def __mul__(self, other: Union[int, float, "Vector"]) -> Union["Vector", float]:
        """
        Умножение вектора на скаляр или скалярное произведение векторов.

        :param other: число (int/float) или другой Vector
        :return: новый Vector (умножение на число) или float (скалярное произведение)
        :raises ValueError: если при векторном умножении размерности не совпадают
        :raises TypeError: если тип other не поддерживается
        """
        if isinstance(other, (int, float)):
            # Умножение на скаляр: каждая координата умножается на число
            new_coords = tuple(c * other for c in self._coords)
            return Vector(*new_coords)

        elif isinstance(other, Vector):
            # Скалярное произведение векторов
            if len(self) != len(other):
                raise ValueError(
                    f"Размерности векторов не совпадают: {len(self)} и {len(other)}"
                )
            return sum(a * b for a, b in zip(self._coords, other._coords))

        else:
            raise TypeError(
                f"Умножение возможно только на число или Vector, получен {type(other)}"
            )

    def __rmul__(self, other: Union[int, float]) -> "Vector":
        """
        Обратное умножение: число * вектор.
        Позволяет писать 5 * v (число слева).
        """
        # Для чисел просто вызываем __mul__
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        return NotImplemented

    @property
    def norm(self) -> float:
        """
        Евклидова норма (длина) вектора.
        Доступна как атрибут без скобок: v.norm

        :return: длина вектора (float)
        """
        return math.sqrt(sum(c**2 for c in self._coords))

    def __eq__(self, other: object) -> bool:
        """Сравнение двух векторов на равенство координат."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self._coords == other._coords



if __name__ == "__main__":
    # Создание векторов
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    v4 = Vector(3, 4)

    print("v1 =", v1)
    print("v2 =", v2)
    print("v4 =", v4)
    print()

    # Сложение
    v3 = v1 + v2
    print("v1 + v2 =", v3)
    print("Ожидается: Vector(5, 7, 9)")
    print()

    # Умножение на число (справа и слева)
    print("v1 * 10 =", v1 * 10)
    print("10 * v1 =", 10 * v1)
    print("Ожидается: Vector(10, 20, 30)")
    print()

    # Скалярное произведение
    dot = v1 * v2
    print("v1 * v2 =", dot)
    print("Ожидается: 32 (1*4 + 2*5 + 3*6)")
    print()

    # Норма (длина)
    print("Длина вектора (3,4):", v4.norm)
    print("Ожидается: 5.0")
    print()

    # Проверка ошибок
    try:
        v_bad = Vector(1, 2)
        result = v1 + v_bad
    except ValueError as e:
        print("Ошибка при сложении векторов разной длины:", e)

    try:
        result = v1 * "строка"
    except TypeError as e:
        print("Ошибка при умножении на неподдерживаемый тип:", e)
"""
Модуль для первичного анализа текстовых данных.

Содержит функцию analyze_text, которая вычисляет базовую статистику
по переданной строке.
"""

import string
from typing import Dict, Union


def analyze_text(text: str) -> Dict[str, Union[int, float]]:

    # Приводим к нижнему регистру
    cleaned_text = text.lower()

    # Удаляем все знаки препинания
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = cleaned_text.translate(translator)

    # Разбиваем на слова по пробельным символам
    words = cleaned_text.split()

    # Общее количество слов
    total_words = len(words)

    # Количество уникальных слов
    unique_words = len(set(words))

    # Средняя длина слова (если слов нет, возвращаем 0.0)
    if total_words == 0:
        avg_word_length = 0.0
    else:
        total_length = sum(len(word) for word in words)
        avg_word_length = round(total_length / total_words, 2)

    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'avg_word_length': avg_word_length,
    }
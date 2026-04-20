import csv
import random
from pathlib import Path
import argparse
from faker import Faker


fake = Faker()

CATEGORIES = [
    "Electronics", "Books", "Clothing", "Food", "Transport",
    "Health", "Entertainment", "Utilities"
]
CURRENCIES = ["RUB", "USD", "EUR"]


def generate_transaction():
    return {
        "id": fake.uuid4(),
        "amount": round(random.uniform(10.0, 50000.0), 2),
        "category": random.choice(CATEGORIES),
        "date": fake.date_between(
            start_date='-5y', end_date='today'
        ).isoformat(),
        "currency": random.choice(CURRENCIES)
    }


def generate_big_csv(output_path: str, target_size_gb: float = 1.0):
    """Генерирует CSV файл заданного размера (приблизительно)."""
    output = Path(output_path)
    target_bytes = int(target_size_gb * 1024 * 1024 * 1024)

    with open(output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "amount", "category", "date", "currency"]
        )
        writer.writeheader()

        sample_row = generate_transaction()
        sample_line = (
            ','.join(str(sample_row[k]) for k in writer.fieldnames) + '\n'
        )
        row_size = len(sample_line.encode('utf-8'))
        rows_needed = target_bytes // row_size

        print(
            f"Генерация примерно {rows_needed:,} строк "
            f"(около {target_size_gb} ГБ)..."
        )
        for i in range(rows_needed):
            writer.writerow(generate_transaction())
            if i % 100000 == 0:
                print(f"  Прогресс: {i:,} / {rows_needed:,} строк")
    file_size_gb = output.stat().st_size / 1024**3
    print(f"Файл сохранён: {output} (размер: {file_size_gb:.2f} ГБ)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Генератор большого CSV для тестирования памяти"
    )
    parser.add_argument("output", help="Путь для выходного файла")
    parser.add_argument(
        "--size", type=float, default=1.0,
        help="Размер в ГБ (по умолчанию 1.0)"
    )
    args = parser.parse_args()
    generate_big_csv(args.output, args.size)

import sys
import logging
import json
from pathlib import Path
from typing import List, Iterator
import tempfile
import shutil

from app.core.models import Transaction
from app.core.exceptions import BaseAppError, DataFormatError
from app.io.reader_registry import ReaderRegistry
from app.services.pipeline import parse_and_validate_stream
from app.services.aggregator import aggregate_stream
from app.services.report import ProcessingReport  # оставляем из ЛР3
from app.utils.memory_profiler import track_memory_peak

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def process_file_stream(file_path: Path, report: ProcessingReport) -> Iterator[Transaction]:
    """Обрабатывает файл с использованием генераторов."""
    extension = file_path.suffix
    try:
        reader_class = ReaderRegistry.get_reader(extension)
        reader = reader_class()
        # Возвращаем генератор валидных транзакций
        return parse_and_validate_stream(str(file_path), reader, expected_currency="RUB")
    except (DataFormatError, ValueError) as e:
        report.add_error(str(file_path), f"Ошибка чтения/формата: {e}")
        return iter([])  # пустой итератор
    except Exception as e:
        report.add_error(str(file_path), f"Неизвестная ошибка: {e}")
        logger.exception(f"Unexpected error reading {file_path}")
        return iter([])


def main():
    data_dir = Path("data")
    if not data_dir.exists():
        logger.error(f"Директория '{data_dir}' не найдена.")
        sys.exit(1)

    report = ProcessingReport()
    all_transactions: Iterator[Transaction] = iter([])

    # Собираем единый поток транзакций из всех файлов
    for file_path in data_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ('.csv', '.json'):
            logger.info(f"Обработка файла: {file_path}")
            file_stream = process_file_stream(file_path, report)
            # Объединяем итераторы (цепочка генераторов)
            # Здесь мы не выполняем итерацию, просто строим конвейер
            def chain(prev, new):
                yield from prev
                yield from new
            all_transactions = chain(all_transactions, file_stream)

    # Агрегация с замером памяти
    with track_memory_peak():
        aggregated = aggregate_stream(all_transactions)

    # Вывод отчёта
    report.print_summary()
    print("\nАгрегированные данные по категориям:")
    for cat, total in aggregated.items():
        print(f"  {cat}: {total:.2f} RUB")

    # Транзакционная запись результата
    output_file = Path("result.json")
    tmp_file = Path("result.json.tmp")
    try:
        with open(tmp_file, 'w', encoding='utf-8') as f:
            json.dump(aggregated, f, ensure_ascii=False, indent=2)
        tmp_file.replace(output_file)
        logger.info(f"Результат сохранён в {output_file}")
    except Exception as e:
        logger.exception(f"Ошибка при сохранении результата: {e}")
        if tmp_file.exists():
            tmp_file.unlink()
        sys.exit(1)


if __name__ == "__main__":
    main()
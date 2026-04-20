import csv
from pathlib import Path
from typing import Iterator
from app.core.models import Transaction
from app.core.exceptions import DataFormatError
from app.io.base_reader import BaseReader

class CSVReader(BaseReader):
    def read(self, file_path: str) -> Iterator[Transaction]:
        path = Path(file_path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    raise DataFormatError(f"CSV файл {file_path} не содержит заголовков")
                required = {'id', 'amount', 'category', 'date'}
                if not required.issubset(set(reader.fieldnames)):
                    missing = required - set(reader.fieldnames)
                    raise DataFormatError(f"Отсутствуют обязательные колонки: {missing}")

                for row_num, row in enumerate(reader, start=2):
                    try:
                        yield Transaction(
                            id=row['id'].strip(),
                            amount=float(row['amount']),
                            category=row['category'].strip(),
                            date=row['date'].strip(),
                            currency=row.get('currency', 'RUB').strip()
                        )
                    except ValueError as e:
                        # Логируем ошибку строки и пропускаем её (graceful degradation)
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.warning(f"Пропущена строка {row_num} в {file_path}: {e}")
                        continue
        except (OSError, UnicodeDecodeError) as e:
            raise DataFormatError(f"Не удалось прочитать CSV файл {file_path}: {e}") from e
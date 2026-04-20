from dataclasses import dataclass, field
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ProcessingReport:
    total_files: int = 0
    success_files: int = 0
    error_files: int = 0
    errors: List[str] = field(default_factory=list)

    def add_success(self):
        self.success_files += 1
        self.total_files += 1

    def add_error(self, file_path: str, error_msg: str):
        self.error_files += 1
        self.total_files += 1
        full_error = f"{file_path}: {error_msg}"
        self.errors.append(full_error)
        logger.error(full_error)

    def print_summary(self):
        print("\n" + "="*50)
        print(f"Обработано файлов: {self.total_files}")
        print(f"Успешно: {self.success_files}")
        print(f"Ошибок: {self.error_files}")
        if self.errors:
            print("Список ошибок:")
            for err in self.errors:
                print(f"  - {err}")
        print("="*50)
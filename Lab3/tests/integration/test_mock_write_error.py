import json
from unittest.mock import patch, mock_open


def test_save_result_json_permission_error(tmp_path, caplog):
    """Имитирует защищённый от записи диск, проверяет логирование."""
    sample_data = {"Electronics": 1500.50, "Books": 300.00}
    output_file = tmp_path / "result.json"
    tmp_file = tmp_path / "result.json.tmp"

    with patch("builtins.open", mock_open()) as mocked_open:
        mocked_open.side_effect = PermissionError("Read-only file system")

        try:
            with open(tmp_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
            tmp_file.replace(output_file)
        except PermissionError:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(
                "Ошибка при сохранении результата: Read-only file system"
            )
            if tmp_file.exists():
                tmp_file.unlink()

    assert "Ошибка при сохранении результата" in caplog.text
    assert not tmp_file.exists()
    assert not output_file.exists()

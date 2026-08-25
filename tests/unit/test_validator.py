import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from services.validator import validate_file, get_file_extension, validate_file_size


class TestValidateFile:
    def test_valid_xlsx(self):
        assert validate_file('xlsx', {'xlsx', 'xls', 'pdf', 'csv'}) is True

    def test_valid_xls(self):
        assert validate_file('xls', {'xlsx', 'xls', 'pdf', 'csv'}) is True

    def test_valid_pdf(self):
        assert validate_file('pdf', {'xlsx', 'xls', 'pdf', 'csv'}) is True

    def test_valid_csv(self):
        assert validate_file('csv', {'xlsx', 'xls', 'pdf', 'csv'}) is True

    def test_invalid_docx_rejected(self):
        assert validate_file('docx', {'xlsx', 'xls', 'pdf', 'csv'}) is False

    def test_invalid_txt_rejected(self):
        assert validate_file('txt', {'xlsx', 'xls', 'pdf', 'csv'}) is False

    def test_case_insensitive(self):
        assert validate_file('XLSX', {'xlsx', 'xls', 'pdf', 'csv'}) is True


class TestGetFileExtension:
    def test_simple_filename(self):
        assert get_file_extension('activity.xlsx') == 'xlsx'

    def test_uppercase_extension_lowered(self):
        assert get_file_extension('ACTIVITY.PDF') == 'pdf'

    def test_no_extension_returns_empty(self):
        assert get_file_extension('fichier_sans_extension') == ''

    def test_multiple_dots(self):
        assert get_file_extension('mon.fichier.test.csv') == 'csv'


class TestValidateFileSize:
    def test_size_under_limit_accepted(self, tmp_path):
        f = tmp_path / 'small.bin'
        f.write_bytes(b'x' * 100)
        with open(f, 'rb') as fh:
            assert validate_file_size(fh, 1024) is True

    def test_size_over_limit_rejected(self, tmp_path):
        f = tmp_path / 'big.bin'
        f.write_bytes(b'x' * 2048)
        with open(f, 'rb') as fh:
            assert validate_file_size(fh, 1024) is False

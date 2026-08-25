import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from openpyxl import Workbook

from services.file_parser import parse_file, get_file_extension, parse_csv, parse_xlsx


def build_xlsx_bytes(rows):
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


class TestGetFileExtension:
    def test_extension_simple(self):
        assert get_file_extension('suivi.xlsx') == 'xlsx'

    def test_sans_extension(self):
        assert get_file_extension('fichier') == ''


class TestParseCsv:
    def test_parse_csv_utf8(self):
        content = b'status,conformite\nvalide,oui\ninconforme,non\n'
        df = parse_csv(io.BytesIO(content))
        assert list(df.columns) == ['status', 'conformite']
        assert len(df) == 2

    def test_parse_csv_latin1_fallback(self):
        content = b'statut,nom\nvalid\xe9,POS-Test\n'  # é en latin-1
        df = parse_csv(io.BytesIO(content))
        assert len(df) == 1


class TestParseXlsx:
    def test_parse_xlsx_valide(self):
        data = build_xlsx_bytes([
            ['status', 'conformite'],
            ['valide', 'oui'],
            ['en attente', 'non'],
        ])
        df = parse_xlsx(data)
        assert list(df.columns) == ['status', 'conformite']
        assert len(df) == 2

    def test_parse_xlsx_corrompu_leve_exception(self):
        corrupt = io.BytesIO(b'Ceci nest pas un fichier excel')
        with pytest.raises(Exception):
            parse_xlsx(corrupt)


class TestDispatchParseFile:
    def test_dispatch_csv_par_nom(self):
        content = b'status\nvalide\n'
        df = parse_file(io.BytesIO(content), 'activite.csv')
        assert len(df) == 1

    def test_format_inconnu_leve_valueerror(self):
        with pytest.raises(ValueError):
            parse_file(io.BytesIO(b'x'), 'document.docx')

    def test_format_xls_route_parse_excel(self):
        # Un .xls malformé doit lever une exception de parsing (pas ValueError de dispatch)
        with pytest.raises(Exception) as excinfo:
            parse_file(io.BytesIO(b'pas un xls'), 'legacy.xls')
        assert not isinstance(excinfo.value, ValueError) or 'Format non supporté' not in str(excinfo.value)

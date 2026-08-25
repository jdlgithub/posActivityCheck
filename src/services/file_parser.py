import pandas as pd
from io import BytesIO
import openpyxl
import xlrd
import tabula
import os

def parse_file(file, filename: str) -> pd.DataFrame:
    extension = get_file_extension(filename)
    
    if extension == 'xlsx':
        return parse_xlsx(file)
    elif extension == 'xls':
        return parse_xls(file)
    elif extension == 'csv':
        return parse_csv(file)
    elif extension == 'pdf':
        return parse_pdf(file)
    else:
        raise ValueError(f'Format non supporté: {extension}')

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lstrip('.').lower()

def parse_xlsx(file) -> pd.DataFrame:
    return pd.read_excel(file, engine='openpyxl')

def parse_xls(file) -> pd.DataFrame:
    return pd.read_excel(file, engine='xlrd')

def parse_csv(file) -> pd.DataFrame:
    return pd.read_csv(file, encoding='utf-8')

def parse_pdf(file) -> pd.DataFrame:
    tables = tabula.read_pdf(file, pages='all', multiple_tables=True)
    if tables:
        return pd.concat(tables, ignore_index=True)
    return pd.DataFrame()
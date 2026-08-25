# Research - Static File Analyzer

**Date**: 2025-08-25
**Status**: Complete

## File Format Support

### .xlsx (Excel 2007+)
- **Library**: openpyxl
- **Rationale**: Standard Python library for .xlsx, maintained, supports all modern Excel features
- **Alternatives**: pandas (heavier), xlwings (requires Excel)
- **Decision**: openpyxl for parsing, pandas for data manipulation

### .xls (Excel 97-2003)
- **Library**: xlrd
- **Rationale**: Legacy format, xlrd is the de facto standard
- **Alternatives**: pandas (built-in support)
- **Decision**: xlrd for dedicated .xls parsing

### .csv (Comma-Separated Values)
- **Library**: pandas
- **Rationale**: Robust parsing with encoding detection, handles various delimiters
- **Alternatives**: csv module (stdlib), pandas (more features)
- **Decision**: pandas for consistency with other formats

### .pdf (Portable Document Format)
- **Library**: tabula-py + pandas
- **Rationale**: tabula-py is Python wrapper for tabula-java, extracts tables from PDF
- **Alternatives**: PyPDF2 (text extraction only, no tables), pdfplumber (Python-based, no Java dependency)
- **Decision**: tabula-py for table extraction; fallback to pdfplumber if Java not available

## UI Framework Selection

### Bootstrap 5 + Custom CSS
- **Rationale**: Professional look, responsive grid, ready-made components
- **Alternatives**: Tailwind CSS (more customization), Material UI (heavier)
- **Decision**: Bootstrap 5 for rapid professional UI

## Performance

### File Processing
- **Target**: <10 seconds for 10,000 row files
- **Strategy**: 
  - Streaming read for large files
  - Lazy evaluation of statistics
  - Chunked processing for CSV
- **Memory**: Limit to 50MB file size

## Error Handling

### Invalid Files
- **Strategy**: Catch parsing exceptions, return user-friendly error
- **Messages**: Clear indication of format mismatch

### Corrupted Files
- **Strategy**: Try/except around parser, log error, show message
- **Logging**: JSON structured logs to stdout

## Security

### File Upload
- **Strategy**: 
  - Validate file extension before processing
  - Limit file size (50MB max)
  - No file persistence (process in memory)
  - No code execution from file content
- **Rationale**: Single-user tool, no network exposure

## Deployment

### Flask App
- **Mode**: Development server for now (can be upgraded to Gunicorn)
- **Static files**: Served by Flask (for production, use WhiteNoise or reverse proxy)
- **Environment**: Python 3.11+, pip install requirements.txt

## Research Summary

| Area | Decision | Confidence |
|------|----------|------------|
| .xlsx parsing | openpyxl | High |
| .xls parsing | xlrd | High |
| .csv parsing | pandas | High |
| .pdf parsing | tabula-py | Medium |
| UI | Bootstrap 5 | High |
| Performance | <10s for 10k rows | High |
| Security | No persistence, size limit | High |
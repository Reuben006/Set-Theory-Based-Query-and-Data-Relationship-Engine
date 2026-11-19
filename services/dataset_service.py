import pandas as pd

from config import PAGE_SIZE_DEFAULT, PAGE_SIZE_MAX
from services.common import is_missing
from utils import ApiError, df_to_rows


def read_csv_file(file_storage):
    if not file_storage or not file_storage.filename:
        raise ApiError("Choose a CSV file.")
    if not file_storage.filename.lower().endswith(".csv"):
        raise ApiError("Only .csv files are allowed.")
    try:
        df = pd.read_csv(file_storage, encoding="utf-8")
    except UnicodeDecodeError:
        file_storage.seek(0)
        df = pd.read_csv(file_storage, encoding="latin-1")
    except (pd.errors.EmptyDataError, pd.errors.ParserError, ValueError):
        raise ApiError("CSV file could not be read.")
    df.columns = [str(column).strip() for column in df.columns]
    if not len(df.columns):
        raise ApiError("CSV file has no columns.")
    if df.empty:
        raise ApiError("CSV file is empty.")
    return df


def describe_columns(df):
    return [{"name": column, "dtype": str(df[column].dtype), "missing": sum(is_missing(value) for value in df[column]), "unique": len({str(value) for value in df[column] if not is_missing(value)})} for column in df.columns]


def quality_report(df):
    duplicates = df.duplicated()
    sample = [{"row": index + 1, "values": df_to_rows(df.iloc[[index]])[0]} for index, duplicate in enumerate(duplicates) if duplicate][:20]
    columns = []
    for column in df.columns:
        values = [str(value) for value in df[column] if not is_missing(value)]
        columns.append({"name": column, "missing": sum(is_missing(value) for value in df[column]), "duplicate_values": len(values) - len(set(values))})
    return {"total_rows": len(df), "duplicate_rows": int(duplicates.sum()), "duplicate_rows_sample": sample, "missing_total": sum(item["missing"] for item in columns), "columns": columns}


def page_rows(df, page, page_size):
    page = max(1, int(page or 1))
    page_size = min(PAGE_SIZE_MAX, max(1, int(page_size or PAGE_SIZE_DEFAULT)))
    total_rows = len(df)
    total_pages = max(1, (total_rows + page_size - 1) // page_size)
    page = min(page, total_pages)
    start = (page - 1) * page_size
    return {"columns": list(df.columns), "rows": df_to_rows(df.iloc[start:start + page_size]), "page": page, "page_size": page_size, "total_rows": total_rows, "total_pages": total_pages}

from datetime import datetime

from utils import ApiError

datasets = {}
results = {}
dataset_number = 0
result_number = 0


def add_dataset(name, df):
    global dataset_number
    dataset_number += 1
    dataset_id = f"d{dataset_number}"
    datasets[dataset_id] = {"id": dataset_id, "name": name, "df": df, "uploaded_at": timestamp()}
    return dataset_id


def get_dataset(dataset_id):
    if dataset_id not in datasets:
        raise ApiError(f"Dataset {dataset_id} not found.", 404)
    return datasets[dataset_id]


def list_datasets():
    return list(datasets.values())


def delete_dataset(dataset_id):
    get_dataset(dataset_id)
    del datasets[dataset_id]


def add_result(kind, label, export_df, stats, summary, extra=None):
    global result_number
    result_number += 1
    result_id = f"r{result_number}"
    results[result_id] = {"id": result_id, "kind": kind, "label": label, "export_df": export_df, "stats": stats, "summary": summary, "extra": extra or {}, "created_at": timestamp()}
    return result_id


def get_result(result_id):
    if result_id not in results:
        raise ApiError(f"Result {result_id} not found.", 404)
    return results[result_id]


def list_results():
    return list(reversed(list(results.values())))


def clear_all():
    global dataset_number, result_number
    datasets.clear()
    results.clear()
    dataset_number = 0
    result_number = 0


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

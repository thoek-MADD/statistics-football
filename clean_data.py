import json
import pandas as pd
from pathlib import Path

from pandas.core.frame import DataFrame


def get_required_columns(reference_json):

    relevant_cols = []
    required_cols = []

    with open(reference_json, "r") as read_file:
        data = json.load(read_file)

        for col in data["columns"]:
            if col["relevant"] == True:
                relevant_cols.append(col["name"])

            if col["required"] == True:
                required_cols.append(col["name"])

    return {
        "relevant": relevant_cols,
        "required": required_cols
    }


def try_open_file_as_DataFrame(url):

    create_df_succes = False
    df = None

    try:
        df = pd.read_csv(
            url,
            sep=",",
            lineterminator="\n"
        )
        create_df_succes = True
    except:
        pass

    return {
        'succes': create_df_succes,
        'file': df
    }


def check_if_col_in_data_frame(name: str, data_frame: DataFrame) -> bool:
    for column in data_frame:
        if data_frame[column].name == name:
            return True

    return False


def file_contains_required_data(required_cols: list, data_frame: DataFrame) -> bool:
    for required in required_cols:
        if not check_if_col_in_data_frame(required, data_frame):
            return False

    return True


def remove_unwanted_cols(relevant_cols: list, data_frame: DataFrame):
    for column in data_frame:
        col_name = data_frame[column].name
        matched_w_relevant = False

        for relevant_col_name in relevant_cols:
            if relevant_col_name == col_name:
                matched_w_relevant = True
                break

        if not matched_w_relevant:
            data_frame.drop(columns=[col_name], inplace=True)


wanted_cols = get_required_columns("data_info.json")
dir = Path("data-copy")

for path in dir.glob("**/*"):
    csv_result = try_open_file_as_DataFrame(path.resolve())

    if csv_result['succes'] == True:
        csv: DataFrame = csv_result['file']

        if not file_contains_required_data(wanted_cols["required"], csv):
            Path.unlink(path)

        else:
            print("\n" + path.name + "\n")
            remove_unwanted_cols(wanted_cols["relevant"], csv)
            csv.to_csv(path.resolve())

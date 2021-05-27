import json
import unicodedata

import pandas as pd

with open("../data/notis.json") as f:
    notis = json.load(f)
notis_df = pd.DataFrame(notis)


def get_news_id(title):
    print(title)
    print("----------------")
    return int(notis_df[notis_df["data_title"] == title]["id"].values)


# aggregate politics preferences into bigger groups (izquierda, derecha, centro)
def aggregate_politics(val):
    if val in ["Izquierda", "Centro izquierda"]:
        return "Izquierda"
    elif val in ["Derecha", "Centro derecha"]:
        return "Derecha"
    elif val == "Centro":
        return val
    else:
        return "NS/NC"


# aggregate ages into bigger groups (18-34, 35-54, 54>)
def aggregate_age(val):
    if val in ["< 18 años", "18-24 años", "25-34 años"]:
        return "<=18-34"
    elif val in ["35-44 años", "45-54 años"]:
        return "35-54"
    elif val in ["55-65 años", "> 65 años"]:
        return "55>"
    elif val is None:
        return None


def prep(df_raw):

    # merge news info
    df_raw = pd.merge(
        df_raw,
        notis_df,
        how="left",
        left_on="fake_news",
        right_on="data_title",
        suffixes=[None, "_fake"],
    )
    df_raw = df_raw.rename(
        columns={
            "news_id": "fake_news_id",
            "topic_1": "fake_topic_1",
            "topic_2": "fake_topic_2",
            "data_title": "fake_news_title",
            "min_title": "fake_news_title_min",
        }
    )
    df_raw = pd.merge(
        df_raw,
        notis_df,
        how="left",
        left_on="true_news",
        right_on="data_title",
        suffixes=[None, "_true"],
    )
    df_raw = df_raw.rename(
        columns={
            "news_id": "true_news_id",
            "topic_1": "true_topic_1",
            "topic_2": "true_topic_2",
            "data_title": "true_news_title",
            "min_title": "true_news_title_min",
        }
    )

    # convert to datetime columns to type datetime
    df_raw["dt_arrive"] = pd.to_datetime(df_raw["date_arrive"])
    df_raw["dt_finish"] = pd.to_datetime(df_raw["date_finish"])

    # create a new variable to store time completion (in minutes)
    df_raw["time_completion_min"] = df_raw.apply(
        lambda row: round((row["dt_finish"] - row["dt_arrive"]).seconds / 60, 3), axis=1
    )

    df_raw["dm_edad_a"] = df_raw["dm_edad"].apply(aggregate_age)

    df_raw["dm_politica_a"] = df_raw["dm_politica"].apply(aggregate_politics)

    df_raw["dm_lugar"] = df_raw.apply(
        lambda row: row["dm_provincia"]
        if row["dm_provincia"] != "Fuera de España"
        else unicodedata.normalize("NFD", row["dm_prov_otro"].strip().title())
        .encode("ascii", "ignore")
        .decode(),
        axis=1,
    )
    df_raw["dm_lugar_country"] = df_raw.apply(
        lambda row: row["dm_prov_otro"]
        if row["dm_provincia"] == "Fuera de España"
        else "España",
        axis=1,
    )
    # TODO [CCAA]

    df_raw["dm_education"] = df_raw.apply(
        lambda row: row["dm_educacion"]
        if row["dm_educacion"] != "Otro"
        else row["dm_edu_otro"].strip().title(),
        axis=1,
    )
    df_raw["dm_employment"] = df_raw.apply(
        lambda row: row["dm_empleo"]
        if row["dm_empleo"] != "Otro"
        else row["dm_empleo_otro"].strip().title(),
        axis=1,
    )
    df_raw["dm_pref_religion"] = df_raw.apply(
        lambda row: row["dm_religion"]
        if row["dm_religion"] != "Otro"
        else row["dm_rel_otro"].strip().title(),
        axis=1,
    )

    fin = ~df_raw["date_finish"].isnull()  # finished experiments
    ini = df_raw["time_index"] > 0  # initiated or read news 1
    read_only_1 = ini & (df_raw["time_news1"] == 0)  # read both news
    read_both = df_raw["time_news1"] > 0  # read both news
    got_to_ans = df_raw["time_news2"] > 0  # read both news and got to ans

    df_all = df_raw
    df_init = df_raw[ini]
    df = df_raw[fin]

    n = df.shape[0]

    vars_all = list(df.columns)
    # print(f"Hay {len(vars_all)} variables:")
    # for idx, var in enumerate(vars_all):
    #     print(f"{idx + 1}. {var}")

    # collect demographic variables
    vars_demo = []
    for var in vars_all:
        if "dm_" in var:
            vars_demo.append(var)

    vars_routine = [
        "rutina_tele",
        "rutina_internet",
        "rutina_redes",
        "rutina_libros",
        "rutina_whatsapp",
        "rutina_radio",
    ]

    return (
        df,
        df_init,
        df_all,
        n,
        fin,
        ini,
        read_only_1,
        read_both,
        got_to_ans,
        vars_all,
        vars_demo,
        vars_routine,
    )

from datetime import datetime, timedelta

import polars as pl

start_datetime = datetime.fromisoformat("2023-09-06 12:51:28.888946")
phase = timedelta(minutes=2)


def to_secs(s):
    return timedelta(seconds=s) + start_datetime


def add_phase(s):
    return timedelta(seconds=s) + start_datetime + phase


df = pl.read_csv(
    "./data/verification_data_load.txt",
    separator="\t",
)
df = df.select(["Zeit  1 - Standardmessrate [s]", "F_machine [kN]"])
df = df.rename({"Zeit  1 - Standardmessrate [s]": "time", "F_machine [kN]": "load"})
df = df.with_columns(pl.all().str.replace(",", ".").cast(float))
df.write_csv("data/verification_load_relative_time.csv")

df_time = df.with_columns(pl.col("time [s]").map_elements(to_secs))
df_time.write_csv("data/verification_load.csv")

df_phase = df.with_columns(pl.col("time [s]").map_elements(to_secs))
df_phase.write_csv("data/verification_load_shifted.csv")

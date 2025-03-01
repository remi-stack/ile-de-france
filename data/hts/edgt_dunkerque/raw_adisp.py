from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
import geopandas as gpd
import os

"""
This stage loads the raw data of the specified HTS (EDGT Lyon).

Adapted from the first implementation by Valentin Le Besond (IFSTTAR Nantes)
"""

def configure(context):
    context.config("data_path")

HOUSEHOLD_COLUMNS = {
    "ECH": str, "ZFM": str, # id
    "M6": int, "M21": int, "M14": int,  # number_of_cars, number_of_bikes, number_of_motorbikes
    "COE0": float # weights
}

PERSON_COLUMNS = {
    "ECH": str, "PER": int, "ZFP": str, # id
    "PENQ": str, # respondents of travel questionary section
    "P2": int, "P4": int, # sex, age
    "P9": str, # employed, studies
    "P7": str, "P12": str, # has_license, has_pt_subscription
    "PCSC": str, # socioprofessional_class
    "COEP": float, "COE1": float # weights
}

TRIP_COLUMNS = {
    "ECH": str, "PER": int, "NDEP": int, "ZFD": str, # id
    "D2A": int, "D5A": int, # preceding_purpose, following_purpose
    "D3": str, "D7": str, # origin_zone, destination_zone
    "D4": int, "D8": int, # time_departure, time_arrival
    "MODP": int, "D11": int, "D12": int # mode, euclidean_distance, routed_distance
}

def execute(context):
    # Load households
    df_households = pd.concat([
        pd.read_csv(
            "%s/edgt_dunkerque/dunkerque_2015_std_faf_men.csv"
            % context.config("data_path"), sep=";", usecols = list(HOUSEHOLD_COLUMNS.keys()), dtype = HOUSEHOLD_COLUMNS
        ),
        pd.read_csv(
            "%s/edgt_dunkerque/dunkerque_2015_std_tel_men.csv"
            % context.config("data_path"), sep=";", usecols = list(HOUSEHOLD_COLUMNS.keys()), dtype = HOUSEHOLD_COLUMNS
        )
    ])

    # Load persons
    df_persons = pd.concat([
        pd.read_csv(
            "%s/edgt_dunkerque/dunkerque_2015_std_faf_pers.csv"
            % context.config("data_path"), sep=";", usecols = list(PERSON_COLUMNS.keys()), dtype = PERSON_COLUMNS
        ),
        pd.read_csv(
            "%s/edgt_dunkerque/dunkerque_2015_std_tel_pers.csv"
            % context.config("data_path"), sep=";", usecols = list(PERSON_COLUMNS.keys()), dtype = PERSON_COLUMNS
        )
    ])

    # Load trips
    df_trips = pd.concat([
        pd.read_csv(
            "%s/edgt_dunkerque/dunkerque_2015_std_faf_depl.csv"
            % context.config("data_path"), sep=";", usecols = list(TRIP_COLUMNS.keys()), dtype = TRIP_COLUMNS
        ),
        pd.read_csv(
            "%s/edgt_dunkerque/dunkerque_2015_std_tel_depl.csv"
            % context.config("data_path"), sep=";", usecols = list(TRIP_COLUMNS.keys()), dtype = TRIP_COLUMNS
        )
    ])

    # Load spatial data
    df_spatial = gpd.read_file(
        "%s/edgt_dunkerque/EDGT_Dunkerque_2015_ZF.TAB"
        % context.config("data_path"))

    return df_households, df_persons, df_trips, df_spatial

FILES = [
    "dunkerque_2015_std_faf_men.csv",
    "dunkerque_2015_std_tel_men.csv",
    "dunkerque_2015_std_faf_pers.csv",
    "dunkerque_2015_std_tel_pers.csv",
    "dunkerque_2015_std_faf_depl.csv",
    "dunkerque_2015_std_tel_depl.csv",
    "EDGT_Dunkerque_2015_ZF.DAT",
    "EDGT_Dunkerque_2015_ZF.ID",
    "EDGT_Dunkerque_2015_ZF.MAP",
    "EDGT_Dunkerque_2015_ZF.TAB"
]

def validate(context):
    for name in FILES:
        if not os.path.exists("%s/edgt_dunkerque/%s" % (context.config("data_path"), name)):
            raise RuntimeError("File missing from EDGT: %s" % name)

    return [
        os.path.getsize("%s/edgt_dunkerque/%s" % (context.config("data_path"), name))
        for name in FILES
    ]
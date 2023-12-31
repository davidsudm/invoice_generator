#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd


def get_remaining_columns(columns):
    """

    :param columns:
    :return:
    """

    # Columns to keep
    columns_to_keep = ["apartment", "first_name", "last_name", "rent", "water", "energy"]
    # Select columns that are not in the specified list
    remaining_columns = [col for col in columns if col not in columns_to_keep]

    return remaining_columns


def get_table_dictionary(dataframe):
    """

    :param dataframe:
    :return:
    """

    dataframe.columns = dataframe.columns.str.lower()

    for col in dataframe.columns:

        if "depa" in col:
            dataframe.rename(columns={col: 'apartment'}, inplace=True)
        elif "nombre" in col:
            dataframe.rename(columns={col: 'first_name'}, inplace=True)
        elif "apellido" in col:
            dataframe.rename(columns={col: 'last_name'}, inplace=True)
        elif "alquiler" in col:
            dataframe.rename(columns={col: 'rent'}, inplace=True)
        elif "agua" in col:
            dataframe.rename(columns={col: 'water'}, inplace=True)
        elif "luz" in col:
            dataframe.rename(columns={col: 'energy'}, inplace=True)

    remaining_columns = get_remaining_columns(dataframe.columns)

    # check remaining_columns are in a even number:
    if len(remaining_columns) % 2 != 0:
        print("Error: Número de columnas addicionales no es par.")
        sys.exit(1)

    paired_list = [(remaining_columns[i], remaining_columns[i + 1]) for i in range(0, len(remaining_columns), 2)]

    for i, (label, amount) in enumerate(paired_list):
        dataframe.rename(columns={label: f'label_{i}'}, inplace=True)
        dataframe.rename(columns={amount: f'amount_{i}'}, inplace=True)

    # remaining columns with new labels
    remaining_columns = get_remaining_columns(dataframe.columns)
    paired_list = [(remaining_columns[i], remaining_columns[i + 1]) for i in range(0, len(remaining_columns), 2)]

    n_decimals = 2
    entries = []

    for index, row in dataframe.iterrows():
        # Fixed label amounts
        # Personal data
        entries_in_row = {'apartment': int(row['apartment']),
                          'first_name': row['first_name'],
                          'last_name': row['last_name'],
                          'rent': "{:.{}f}".format(float(row['rent']), n_decimals),
                          'energy': "{:.{}f}".format(float(row['energy']), n_decimals),
                          'water': "{:.{}f}".format(float(row['water']), n_decimals)
                          }

        # Variable labels and their amounts
        cnt_recoded_label = 0
        for i, (_, _) in enumerate(paired_list):
            label_key = f'label_{cnt_recoded_label}'
            amount_key = f'amount_{cnt_recoded_label}'

            if row[label_key] is not None and row[label_key] != '' and not pd.isna(row[amount_key]):
                if row[amount_key] != 0.0:
                    entries_in_row[label_key] = row[label_key]
                    entries_in_row[amount_key] = np.round(float(row[amount_key]), decimals=n_decimals)
                    cnt_recoded_label += 1

        entries.append(entries_in_row)

    return entries


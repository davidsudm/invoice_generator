#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def create_folder(path):
    """
    Create a directory is path does not exist

    :param path:    path to the directory set for creation
    :return:        None
    """
    try:
        os.makedirs(path)
        print(f"Folder '{path}' created successfully.")
    except FileExistsError:
        print(f"Folder '{path}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def make_invoice(entries):
    """
    Creates invoices for customers using data from a CSV file and saves them as PDF files

    :param entries: (dict) A dictionary containing values for different invoice parameters.
    :return:        None
    """

    # Create ArgumentParser object
    building = entries['property']
    csv_file = entries['csv']
    output_dir = entries['output']
    invoice_year = entries['year']
    invoice_month = entries['month']
    electricity_starting_date = entries['water']['initial']
    electricity_ending_date = entries['water']['final']
    water_starting_date = entries['electricity']['initial']
    water_ending_date = entries['electricity']['final']
    check_1 = bool(entries['column_1']['check'])
    check_2 = bool(entries['column_2']['check'])
    check_3 = bool(entries['column_3']['check'])

    checks = [check_1, check_2, check_3]
    extra_columns = []

    for i, check in enumerate(checks):
        if check is True:
            extra_columns.append(entries[f'column_{i+1}']['label'])
        else:
            extra_columns.append('')

    if building == 'COLQUEPATA':
        building_address = 'Jr. Colquepata 215'
    else:
        building_address = 'Jr. Quipaypampa 227'

    create_folder(output_dir)
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():

        apartment = row['DEPARTAMENTO']
        first_name = row['NOMBRE']
        last_name = row['APELLIDO']
        rent_amount = np.round(float(row['MONTO_ALQUILER']), decimals=1)
        electricity_amount = np.round(float(row['MONTO_LUZ']), decimals=1)
        water_amount = np.round(float(row['MONTO_AGUA']), decimals=1)
        services_amount = np.round(float(row['MONTO_SERVICIO_LIMPIEZA']), decimals=1)

        signature = plt.imread("figures/firma.png")
        im = OffsetImage(signature, zoom=0.50)
        ab = AnnotationBbox(im,
                            xy=[0.72, 0.65],
                            boxcoords=("axes fraction", "data"),
                            box_alignment=(0.5, 0.5),
                            bboxprops=dict(alpha=0.0))

        values = []
        for i, check in enumerate(checks):
            if check is True:
                values.append(row[f'COLUMNA_{i+1}'])
            else:
                values.append(np.nan)

        total_sum = [rent_amount, electricity_amount, water_amount, services_amount, values[0], values[1], values[2]]
        total_sum = np.round(np.nansum(total_sum), decimals=1)

        columns = ('DESCRIPCION', ' MONTO \n[S/.]')
        data = ((f"Renta {invoice_month} {invoice_year}", rent_amount),
                (f"Luz del {electricity_starting_date} al {electricity_ending_date}", electricity_amount),
                (f"Agua del {water_starting_date} al {water_ending_date}", water_amount),
                (f"Servicios y Limpieza de {invoice_month} {invoice_year}", services_amount),
                (extra_columns[0], np.where(np.isnan(values[0]), "", values[0])),
                (extra_columns[1], np.where(np.isnan(values[1]), "", values[1])),
                (extra_columns[2], np.where(np.isnan(values[2]), "", values[2])),
                ("TOTAL", total_sum))

        fig, ax = plt.subplot_mosaic([['A', 'A', 'A', 'A', 'A', 'A', 'A'],
                                      ['A', 'A', 'A', 'A', 'A', 'A', 'A'],
                                      ['C', 'C', 'C', 'C', 'B', 'B', 'B'],
                                      ['C', 'C', 'C', 'C', 'B', 'B', 'B'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['G', 'G', 'G', 'H', 'H', 'H', 'H'],
                                      ['I', 'I', 'I', 'I', 'I', 'I', 'I']],
                                     #layout="constrained",
                                     height_ratios=[0.25, 0.25, 1, 1, 1, 1, 1, 1, 1, 1.5, 0.25],
                                     width_ratios=[0.5, 0.65, 0.65, 1.25, 1.25, 1.25, 0.5],
                                     figsize=(10, 16))

        # Add a table at the bottom of the axes
        the_table = ax['E'].table(cellText=data,
                                  colLabels=columns,
                                  loc='center')
        # Set font size and scale for column labels and cell content
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(18)

        # Manually set column widths
        col_widths = [1.0, 0.20]  # Adjust as needed
        for i, width in enumerate(col_widths):
            for j, row in enumerate(range(len(data) + 1)):
                the_table._cells[(j, i)].set_width(width)

        # Set cell heights
        the_table.auto_set_column_width([2, 1])  # Column 1 has 2 times the width of Column 2
        the_table.scale(1, 4)  # Adjust the scale for cell heights

        # Make the first and last rows bold
        for j in range(2):
            cell_first_row = the_table._cells[(0, j)]
            cell_last_row = the_table._cells[(len(data), j)]

            cell_first_row.set_text_props(weight='bold')
            cell_last_row.set_text_props(weight='bold')

        # Add background color to the first and last rows
        for j in range(2):
            the_table._cells[(0, j)].set_facecolor('#a6a6a6')  # gray background color for the first row
            the_table._cells[(len(data), j)].set_facecolor('#a6a6a6')  # gray background color for the last row

        for subplot in ax.values():
            subplot.axis('off')

        ax['A'].axhline(y=0.95, linewidth=5, color='C0')
        ax['A'].text(0.0, 0.60, 'RECIBO DE PAGO', va='center', color='C0', fontsize=20, weight='bold')
        ax['A'].text(0.0, 0.20, f'{invoice_month} {invoice_year}', va='center', color='C0', fontsize=20, weight='bold')
        ax['I'].axhline(y=0.05, linewidth=5, color='C0')

        ax['B'].text(0.05, 0.90, 'Lugar de', va='center', color='C0', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.80, 'arrendamiento :', va='center', color='C0', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.70, building_address, va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.60, 'Urb. Tahuantinsuyo', va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.50, 'Independencia', va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.40, 'Lima, Perú', va='center', color='gray', fontsize=14, weight='bold')

        ax['C'].text(0.02, 0.90, 'Arrendatario :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.80, last_name, va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.70, first_name, va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.60, '', va='center', color='gray', fontsize=18)
        ax['C'].text(0.02, 0.50, 'Departamento :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.40, apartment, va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.30, '', va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.20, 'Fecha de emisión :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.10, datetime.today().date().strftime("%d/%m/%Y"), va='center', color='gray', fontsize=18, weight='bold')

        ax['G'].text(0.02, 0.85, 'Atentamente,', va='center', color='gray', fontsize=18, weight='bold')

        ax['H'].add_artist(ab)
        ax['H'].text(0.550, 0.22, 'Wuilber Miranda', va='center', color='gray', fontsize=15, weight='bold')
        ax['H'].text(0.565, 0.12, 'Quispecahuana', va='center', color='gray', fontsize=15, weight='bold')
        ax['H'].text(0.500, 0.00, 'Propietario Administrador', va='center', color='gray', fontsize=12, weight='bold')

        plt.savefig(os.path.join(output_dir, f"{invoice_year}_{invoice_month}_depa_{apartment}.pdf"), format="pdf")
        plt.close(fig)

#!/usr/bin/env python

import os
import argparse
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def create_folder(path):
    try:
        os.makedirs(path)
        print(f"Folder '{path}' created successfully.")
    except FileExistsError:
        print(f"Folder '{path}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Creates invoices of costumers using a csv file with data.')
    # Add arguments
    parser.add_argument('--csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('--output_dir', type=str, help='Path to directory where invoices are stored')
    # Parse the command-line arguments
    args = parser.parse_args()
    # Access the parsed arguments
    csv_file = args.csv_file
    output_dir = args.output_dir

    create_folder(output_dir)
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():

        invoice_year = "2023"
        invoice_month = "SETIEMBRE"
        electricity_starting_date = "01/01/2023"
        electricity_ending_date = "31/01/2023"
        water_starting_date = "15/12/2022"
        water_ending_date = "14/01/2023"

        departamento = row['DEPARTAMENTO']
        nombre = row['NOMBRE']
        apellido = row['APELLIDO']
        rent_amount = np.round(float(row['MONTO_ALQUILER'].replace(',', '.')), decimals=1)
        electricity_amount = np.round(float(row['MONTO_LUZ'].replace(',', '.')), decimals=1)
        water_amount = np.round(float(row['MONTO_AGUA'].replace(',', '.')), decimals=1)
        services_amount = np.round(float(row['MONTO_SERVICIO_LIMPIEZA'].replace(',', '.')), decimals=1)
        total = np.round(np.sum([rent_amount, electricity_amount, services_amount, services_amount]), decimals=1)

        signature = plt.imread("figures/firma.png")
        im = OffsetImage(signature, zoom=.85)
        ab = AnnotationBbox(im,
                            xy=[0.72, 0.65],
                            boxcoords=("axes fraction", "data"),
                            box_alignment=(0.5, 0.5),
                            bboxprops=dict(alpha=0.0))

        columns = ('DESCRIPCION', ' MONTO \n[S/.]')
        data = [[f"Renta {invoice_month} {invoice_year}", rent_amount],
                [f"Luz del {electricity_starting_date} al {electricity_ending_date}", electricity_amount],
                [f"Agua del {water_starting_date} al {water_ending_date}", water_amount],
                [f"Servicios y Limpieza de {invoice_month} {invoice_year}", services_amount],
                ["TOTAL", total]
                ]

        fig, ax = plt.subplot_mosaic([['A', 'A', 'A', 'A', 'A', 'A', 'A'],
                                      ['A', 'A', 'A', 'A', 'A', 'A', 'A'],
                                      ['C', 'C', 'C', 'C', 'B', 'B', 'B'],
                                      ['C', 'C', 'C', 'C', 'B', 'B', 'B'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['G', 'G', 'G', 'H', 'H', 'H', 'H'],
                                      ['I', 'I', 'I', 'I', 'I', 'I', 'I']],
                                     #layout="constrained",
                                     height_ratios=[0.25, 0.25, 1, 1, 1, 1, 1, 1.5, 0.25],
                                     width_ratios=[0.5, 0.65, 0.65, 1.25, 1.25, 1.25, 0.5],
                                     figsize=(10, 14))

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
        ax['B'].text(0.05, 0.70, 'Jr. Quipaypampa 227', va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.60, 'Urb. Tahuantinsuyo', va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.50, 'Independencia', va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.40, 'Lima, Perú', va='center', color='gray', fontsize=14, weight='bold')

        ax['C'].text(0.02, 0.90, 'Arrendatario :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.80, apellido, va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.70, nombre, va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.60, '', va='center', color='gray', fontsize=18)
        ax['C'].text(0.02, 0.50, 'Departamento :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.40, departamento, va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.30, '', va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.20, 'Fecha de emisión :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.10, datetime.today().date().strftime("%d/%m/%Y"), va='center', color='gray', fontsize=18, weight='bold')

        ax['G'].text(0.02, 0.85, 'Atentamente,', va='center', color='gray', fontsize=18, weight='bold')

        ax['H'].add_artist(ab)
        ax['H'].text(0.550, 0.22, 'Wuilber Miranda', va='center', color='gray', fontsize=15, weight='bold')
        ax['H'].text(0.565, 0.12, 'Quispecahuana', va='center', color='gray', fontsize=15, weight='bold')
        ax['H'].text(0.500, 0.00, 'Propietario Administrador', va='center', color='gray', fontsize=12, weight='bold')

        plt.savefig(os.path.join(output_dir, f"departamento_{departamento}_{invoice_year}_{invoice_month}.pdf"), format="pdf")
        plt.close(fig)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

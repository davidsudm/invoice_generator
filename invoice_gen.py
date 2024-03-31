#!/usr/bin/env python

import os

import read_table
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


def break_string_at_word(text, max_length):
    lines = []
    current_line = ""

    words = text.split()

    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    # Add the last line
    lines.append(current_line.strip())

    return "\n".join(lines)


def make_invoice(entries):
    """

    :param entries: 
    :return: 
    """

    # Get the absolute path to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Specify the absolute path to the image file
    image_path = os.path.join(script_dir, 'figures', 'firma.png')
    print("Current Working Directory:", os.getcwd())

    building = entries['property']
    excel_file = entries['excel']
    output_dir = entries['output']
    invoice_year = entries['year']
    invoice_month = entries['month']
    water_starting_date = entries['water']['initial']
    water_ending_date = entries['water']['final']
    energy_starting_date = entries['energy']['initial']
    energy_ending_date = entries['energy']['final']

    if building == 'COLQUEPATA':
        building_address = 'Jr. Colquepata 215'
    else:
        building_address = 'Jr. Quipaypampa 227'

    create_folder(output_dir)
    df = pd.DataFrame()

    try:
        df = pd.read_excel(io=excel_file, usecols="A:P", sheet_name="CSV", engine='openpyxl')
    except FileNotFoundError:
        print(f"File '{excel_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    table_dict = read_table.get_table_dictionary(dataframe=df)
    fixed_columns = ['apartment', 'first_name', 'last_name', 'rent', 'energy', 'water']

    for i, client_dict in enumerate(table_dict):

        extra_columns = [key for key in client_dict.keys() if key not in fixed_columns]
        extra_labels = [col for col in extra_columns if "label" in col]
        extra_amounts = [col for col in extra_columns if "amount" in col]

        # If label two long, it is separated in two lines
        for label in extra_labels:
            client_dict[label] = break_string_at_word(text=client_dict[label], max_length=40)

        total_sum = [client_dict[key] for key in extra_amounts]
        total_sum += [float(client_dict['rent']), float(client_dict['energy']), float(client_dict['water'])]
        total_sum = np.nansum(total_sum)

        columns = ('Descripción', ' Monto \n[S/.]')
        data_fixed = [(f"Renta {invoice_month} {invoice_year}", client_dict['rent']),
                      (f"Agua del {water_starting_date} al {water_ending_date}", client_dict['water']),
                      (f"Luz del {energy_starting_date} al {energy_ending_date}", client_dict['energy'])
                      ]
        data_variable = [(client_dict[f'label_{k}'], client_dict[f'amount_{k}']) for k in range(len(extra_labels))]
        data_sum = [("TOTAL", "{:.{}f}".format(total_sum, 2))]

        data = data_fixed + data_variable + data_sum

        signature = plt.imread(image_path)
        im = OffsetImage(signature, zoom=0.50)
        ab = AnnotationBbox(im,
                            xy=[0.72, 0.65],
                            boxcoords=("axes fraction", "data"),
                            box_alignment=(0.5, 0.5),
                            bboxprops=dict(alpha=0.0))

        fig, ax = plt.subplot_mosaic([['A', 'A', 'A', 'A', 'A', 'A', 'A'],
                                      ['A', 'A', 'A', 'A', 'A', 'A', 'A'],
                                      ['C', 'C', 'C', 'C', 'B', 'B', 'B'],
                                      ['C', 'C', 'C', 'C', 'B', 'B', 'B'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['J', 'E', 'E', 'E', 'E', 'E', 'K'],
                                      ['G', 'G', 'G', 'H', 'H', 'H', 'H'],
                                      ['I', 'I', 'I', 'I', 'I', 'I', 'I']],
                                     height_ratios=[0.25, 0.25, 1, 1, 1, 1, 1, 1, 1, 1, 1.5, 0.25],
                                     width_ratios=[0.5, 0.65, 0.65, 1.25, 1.25, 1.25, 0.5],
                                     figsize=(10, 18))

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
        ax['B'].text(0.05, 0.68, building_address, va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.58, 'Urb. Tahuantinsuyo', va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.48, 'Independencia', va='center', color='gray', fontsize=14, weight='bold')
        ax['B'].text(0.05, 0.38, 'Lima, Perú', va='center', color='gray', fontsize=14, weight='bold')

        ax['C'].text(0.02, 0.90, 'Arrendatario :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.78, client_dict["first_name"], va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.68, client_dict["last_name"], va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.58, '', va='center', color='gray', fontsize=18)
        ax['C'].text(0.02, 0.50, 'Departamento :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.38, client_dict["apartment"], va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.30, '', va='center', color='gray', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.20, 'Fecha de emisión :', va='center', color='C0', fontsize=18, weight='bold')
        ax['C'].text(0.02, 0.08, datetime.today().date().strftime("%d/%m/%Y"), va='center', color='gray', fontsize=18, weight='bold')

        ax['G'].text(0.02, 0.85, 'Atentamente,', va='center', color='gray', fontsize=18, weight='bold')

        ax['H'].add_artist(ab)
        ax['H'].text(0.72, 0.22, 'Wuilber Miranda\nQuispecahuana', va='center', ha='center', color='gray', fontsize=15, weight='bold')
        ax['H'].text(0.72, 0.00, 'Propietario y Administrador', va='center', ha='center', color='gray', fontsize=12, weight='bold')

        output_filename = f"{invoice_year}_{invoice_month.lower()}_depa_{client_dict['apartment']}_{client_dict['last_name'].replace(' ', '_').lower()}.pdf"
        plt.savefig(os.path.join(output_dir, output_filename), format="pdf")
        plt.close(fig)

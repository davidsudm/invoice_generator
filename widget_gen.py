#!/usr/bin/env python

import tkinter
from tkinter import ttk, filedialog
from tkcalendar import Calendar
from datetime import datetime
import invoice_gen


def pick_date(entry, window, date_var):
    """
    This function creates a date picker dialog for selecting a date using the Tkinter library in Python. The selected
    date is then displayed in an entry widget and stored in a 'tkinter.StringVar()'.

    :param entry:       The Entry widget where the selected date will be displayed
    :param window:      The main Tkinter window
    :param date_var:    A StringVar to store the selected date
    :return:            None
    """

    def on_date_selected(calendar):
        selected_date = calendar.get_date()
        date_var.set(selected_date)
        entry.delete(0, tkinter.END)
        entry.insert(0, selected_date)
        top.destroy()

    top = tkinter.Toplevel(window)
    top.title("Elige Fecha")
    current_date = datetime.now()
    cal = Calendar(top,
                   selectmode='day',
                   year=current_date.year,
                   month=current_date.month,
                   day=current_date.day,
                   locale='es',
                   showweeknumbers=False,
                   font=('Helvetica', 16))
    cal.grid(row=0, column=0, padx=10, pady=10)
    cal.config(background='lightblue', foreground='black', bordercolor='white')

    select_button = tkinter.Button(top, text="ACEPTAR FECHA", command=lambda: on_date_selected(cal))
    select_button.grid(row=1, column=0, pady=10)


def browse_file(entry_var):
    """
    Opens a file dialog to select a file and updates the provided Entry widget's associated StringVar with the selected
    file path.

    :param entry_var:   The StringVar associated with the Entry widget where the selected file path will be displayed
    :return:            None
    """

    file_path = filedialog.askopenfilename()
    entry_var.set(file_path)


def browse_folder(entry_var):
    """
    Opens a folder dialog to select a directory and updates the provided Entry widget's associated StringVar with the
    selected folder path

    :param entry_var:   The StringVar associated with the Entry widget where the selected folder path will be displayed
    :return:            None
    """

    folder_path = filedialog.askdirectory()
    entry_var.set(folder_path)


def get_widget_entries(property_var, year_var, month_var,
                       water_starting_date_var, water_ending_date_var,
                       energy_starting_date_var, energy_ending_date_var,
                       open_excel_file_entry_var, open_folder_entry_var, window):
    """
    Retrieves values from provided variables associated with different widgets and returns them as a dictionary

    :param property_var:               The StringVar associated with the property ComboBox
    :param year_var:                   The StringVar associated with the year ComboBox
    :param month_var:                  The StringVar associated with the month ComboBox
    :param water_starting_date_var:    The StringVar associated with the water starting date Entry
    :param water_ending_date_var:      The StringVar associated with the water ending date Entry
    :param energy_starting_date_var:   The StringVar associated with the energy starting date Entry
    :param energy_ending_date_var:     The StringVar associated with the energy ending date Entry
    :param open_excel_file_entry_var:    The StringVar associated with the Excel file path Entry
    :param open_folder_entry_var:      The StringVar associated with the folder path Entry
    :param window:                     Main 'Tkinker' window
    :return:                           dict: A dictionary containing the retrieved values from the provided
                                       variables
    """

    # Retrieve values from vars
    entries = {"property": property_var.get(),
               "year": year_var.get(),
               "month": month_var.get(),
               "water": {"initial": water_starting_date_var.get(),
                         "final": water_ending_date_var.get()},
               "energy": {"initial": energy_starting_date_var.get(),
                          "final": energy_ending_date_var.get()},
               "excel": open_excel_file_entry_var.get(),
               "output": open_folder_entry_var.get()
               }

    window.destroy()

    return entries


def run_widget():

    global window
    window = tkinter.Tk()
    window.title("Generador de Recibos")

    style = ttk.Style(window)
    style.theme_use('alt')

    frame = tkinter.Frame(window)
    frame.grid(row=0, column=0, padx=30, pady=20)

    # property : Create a Combobox with two string values
    property_var = tkinter.StringVar()
    property_label = tkinter.Label(frame, text="INMUEBLE")
    property_label.grid(row=0, column=0)
    property_cb = ttk.Combobox(frame, values=["COLQUEPATA", "QUIPAYPAMPA"], state='readonly',
                               textvariable=property_var)
    property_cb.grid(row=1, column=0, padx=10)

    # year : Create a Combobox with years between 2020 and 2050
    year_var = tkinter.StringVar()
    year_label = tkinter.Label(frame, text="AÑO")
    year_label.grid(row=0, column=1)
    years_values = list(range(2020, 2050 + 1))
    year_cb = ttk.Combobox(frame, values=years_values, state='readonly', textvariable=year_var)
    year_cb.grid(row=1, column=1, padx=10)

    # month : Create a Combobox with months in Spanish
    month_var = tkinter.StringVar()
    month_label = tkinter.Label(frame, text="MES")
    month_label.grid(row=0, column=2, pady=10)
    month_values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]
    month_cb = ttk.Combobox(frame, values=month_values, state='readonly', textvariable=month_var)
    month_cb.grid(row=1, column=2, padx=10)

    # Calendar : water
    water_label = tkinter.Label(frame, text="SERVICIO DE AGUA")
    water_label.grid(row=3, column=0, pady=20)

    water_starting_date_var = tkinter.StringVar()
    water_starting_date = tkinter.Entry(frame)
    water_starting_date.grid(row=3, column=2, pady=20)
    pick_date_button_water_o = tkinter.Button(frame, text="FECHA DE INICIO",
                                              command=lambda: pick_date(entry=water_starting_date,
                                                                        date_var=water_starting_date_var,
                                                                        window=window))
    pick_date_button_water_o.grid(row=3, column=1, pady=20)

    water_ending_date_var = tkinter.StringVar()
    water_ending_date = tkinter.Entry(frame)
    water_ending_date.grid(row=4, column=2, pady=2)
    pick_date_button_water_o = tkinter.Button(frame, text="FECHA DE FIN",
                                              command=lambda: pick_date(entry=water_ending_date,
                                                                        date_var=water_ending_date_var,
                                                                        window=window))
    pick_date_button_water_o.grid(row=4, column=1, pady=2)

    # Calendar : energy
    energy_label = tkinter.Label(frame, text="SERVICIO DE LUZ")
    energy_label.grid(row=5, column=0, pady=20)

    energy_starting_date_var = tkinter.StringVar()
    energy_starting_date = tkinter.Entry(frame)
    energy_starting_date.grid(row=5, column=2, pady=20)
    pick_date_button_energy_o = tkinter.Button(frame, text="FECHA DE INICIO",
                                                    command=lambda: pick_date(entry=energy_starting_date,
                                                                              date_var=energy_starting_date_var,
                                                                              window=window))
    pick_date_button_energy_o.grid(row=5, column=1, pady=20)

    energy_ending_date_var = tkinter.StringVar()
    energy_ending_date = tkinter.Entry(frame)
    energy_ending_date.grid(row=6, column=2, pady=2)
    pick_date_button_energy_o = tkinter.Button(frame, text="FECHA DE FIN",
                                                    command=lambda: pick_date(entry=energy_ending_date,
                                                                              date_var=energy_ending_date_var,
                                                                              window=window))
    pick_date_button_energy_o.grid(row=6, column=1, pady=2)

    # excel file
    open_excel_file_entry_var = tkinter.StringVar()
    open_excel_file_entry = tkinter.Entry(frame, textvariable=open_excel_file_entry_var, width=50)
    open_excel_file_button = tkinter.Button(frame,
                                          text="BUSCAR ARCHIVO EXCEL",
                                          command=lambda: browse_file(open_excel_file_entry_var))
    open_excel_file_button.grid(row=7, column=0, sticky="news", padx=20, pady=20)
    open_excel_file_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=20)

    # Saving directory :
    open_folder_entry_var = tkinter.StringVar()
    open_folder_entry = tkinter.Entry(frame, textvariable=open_folder_entry_var, width=50)
    open_folder_button = tkinter.Button(frame,
                                        text="GUARDAR RECIBOS EN CARPETA",
                                        command=lambda: browse_folder(open_folder_entry_var))
    open_folder_button.grid(row=8, column=0, sticky="news", padx=20, pady=20)
    open_folder_entry.grid(row=8, column=1, columnspan=2, padx=10, pady=20)

    # Generate Invoice Button
    gen_invoice_button = tkinter.Button(frame, text="GENERAR RECIBOS",
                                        command=lambda: invoice_gen.make_invoice(get_widget_entries(
                                            property_var=property_var,
                                            year_var=year_var,
                                            month_var=month_var,
                                            water_starting_date_var=water_starting_date_var,
                                            water_ending_date_var=water_ending_date_var,
                                            energy_starting_date_var=energy_starting_date_var,
                                            energy_ending_date_var=energy_ending_date_var,
                                            open_excel_file_entry_var=open_excel_file_entry_var,
                                            open_folder_entry_var=open_folder_entry_var,
                                            window=window))
                                        )
    gen_invoice_button.config(width=20, height=3, fg='green', font=('Helvetica', 16))
    gen_invoice_button.grid(row=16, column=2, sticky="news", padx=20, pady=10)

    window.mainloop()

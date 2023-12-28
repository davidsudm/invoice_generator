import os
import tkinter
from tkinter import ttk, filedialog
from tkcalendar import Calendar
from datetime import datetime


def pick_date(entry, window):
    def on_date_selected(calendar):
        selected_date = calendar.get_date()
        entry.delete(0, tkinter.END)
        entry.insert(0, selected_date)
        top.destroy()

    top = tkinter.Toplevel(window)
    top.title("Elige Fecha")

    current_date = datetime.now()

    cal = Calendar(top, selectmode='day', year=current_date.year, month=current_date.month, day=current_date.day,
                   locale='es', showweeknumbers=False, font=('Helvetica', 16))
    cal.grid(row=0, column=0, padx=10, pady=10)
    cal.config(background='lightblue', foreground='black', bordercolor='white')

    select_button = tkinter.Button(top, text="ACEPTAR FECHA", command=lambda: on_date_selected(cal))
    select_button.grid(row=1, column=0, pady=10)


def browse_file(entry_var):
    file_path = filedialog.askopenfilename()
    entry_var.set(file_path)


def browse_folder(entry_var):
    folder_path = filedialog.askdirectory()
    entry_var.set(folder_path)


def main():


    window = tkinter.Tk()
    window.title("Generador de Recibos")

    style = ttk.Style(window)
    style.theme_use('alt')

    frame = tkinter.Frame(window)
    frame.grid(row=0, column=0, padx=30, pady=20)
    # frame.pack(padx=30, pady=20)

    # Create a Combobox with two string values
    property_label = tkinter.Label(frame, text="INMUEBLE")
    property_label.grid(row=0, column=0)
    property_cb = ttk.Combobox(frame, values=["COLQUEPATA", "QUIPAYPAMPA"], state='readonly')
    property_cb.grid(row=1, column=0, padx=10)

    year_label = tkinter.Label(frame, text="AÑO")
    year_label.grid(row=0, column=1)
    years_values = list(range(2020, 2050 + 1))
    year_cb = ttk.Combobox(frame, values=years_values, state='readonly')
    year_cb.grid(row=1, column=1, padx=10)

    month_label = tkinter.Label(frame, text="MES")
    month_label.grid(row=0, column=2, pady=10)
    month_values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_cb = ttk.Combobox(frame, values=month_values, state='readonly')
    month_cb.grid(row=1, column=2, padx=10)

    # Calendar Button
    water_label = tkinter.Label(frame, text="SERVICIO DE AGUA")
    water_label.grid(row=3, column=0, pady=20)

    water_starting_date = tkinter.Entry(frame)
    water_starting_date.grid(row=3, column=2, pady=20)
    pick_date_button_water_o = tkinter.Button(frame, text="FECHA DE INICIO",
                                              command=lambda: pick_date(water_starting_date, window))
    pick_date_button_water_o.grid(row=3, column=1, pady=20)

    water_ending_date = tkinter.Entry(frame)
    water_ending_date.grid(row=4, column=2, pady=2)
    pick_date_button_water_o = tkinter.Button(frame, text="FECHA DE FIN",
                                              command=lambda: pick_date(water_ending_date, window))
    pick_date_button_water_o.grid(row=4, column=1, pady=2)


    electricity_label = tkinter.Label(frame, text="SERVICIO DE LUZ")
    electricity_label.grid(row=5, column=0, pady=20)

    electricity_starting_date = tkinter.Entry(frame)
    electricity_starting_date.grid(row=5, column=2, pady=20)
    pick_date_button_electricity_o = tkinter.Button(frame, text="FECHA DE INICIO",
                                              command=lambda: pick_date(electricity_starting_date, window))
    pick_date_button_electricity_o.grid(row=5, column=1, pady=20)

    electricity_ending_date = tkinter.Entry(frame)
    electricity_ending_date.grid(row=6, column=2, pady=2)
    pick_date_button_electricity_o = tkinter.Button(frame, text="FECHA DE FIN",
                                              command=lambda: pick_date(electricity_ending_date, window))
    pick_date_button_electricity_o.grid(row=6, column=1, pady=2)

    # Create a StringVar to hold the file path
    open_csv_file_entry_var = tkinter.StringVar()
    # Create an Entry widget to display the selected file path
    open_csv_file_entry = tkinter.Entry(frame, textvariable=open_csv_file_entry_var, width=50)
    open_csv_file_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=20)
    # Open the file dialog
    open_csv_file_button = tkinter.Button(frame, text="BUSCAR TABLERO CSV",
                                          command=lambda: browse_file(open_csv_file_entry_var))
    open_csv_file_button.grid(row=7, column=0, sticky="news", padx=20, pady=20)

    # Create a StringVar to hold the folder path
    open_folder_entry_var = tkinter.StringVar()
    # Create an Entry widget to display the selected folder path
    open_folder_entry = tkinter.Entry(frame, textvariable=open_folder_entry_var, width=50)
    open_folder_entry.grid(row=8, column=1, columnspan=2, padx=10, pady=20)
    # Open the folder dialog
    open_folder_button = tkinter.Button(frame, text="GUARDAR EN CARPETA",
                                        command=lambda: browse_folder(open_folder_entry_var))
    open_folder_button.grid(row=8, column=0, sticky="news", padx=20, pady=20)

    # Optional Columns
    optional_columns = tkinter.Label(frame, text="COLUMNAS ADICIONALES (OPCIONAL)")
    optional_columns.grid(row=9, column=0, columnspan=3, pady=20)

    opt_col_check = tkinter.Label(frame, text="ETIQUETA DE LA COLUMNA")
    opt_col_check.grid(row=10, column=1, columnspan=2, pady=10)

    # Checkbutton example
    check_var_1 = tkinter.IntVar()
    opt_col_1 = tkinter.Checkbutton(frame, text="AGREGAR COLUMNA 1", variable=check_var_1)
    opt_col_1.grid(row=11, column=0, pady=10)
    opt_col_1_label = tkinter.Entry(frame, width=50)
    opt_col_1_label.grid(row=11, column=1, columnspan=2, pady=10)

    check_var_2 = tkinter.IntVar()
    opt_col_2 = tkinter.Checkbutton(frame, text="AGREGAR COLUMNA 2", variable=check_var_2)
    opt_col_2.grid(row=12, column=0, pady=10)
    opt_col_2_label = tkinter.Entry(frame, width=50)
    opt_col_2_label.grid(row=12, column=1, columnspan=2, pady=10)

    check_var_3 = tkinter.IntVar()
    opt_col_3 = tkinter.Checkbutton(frame, text="AGREGAR COLUMNA 3", variable=check_var_3)
    opt_col_3.grid(row=13, column=0, pady=10)
    opt_col_3_label = tkinter.Entry(frame, width=50)
    opt_col_3_label.grid(row=13, column=1, columnspan=2, pady=10)

    gen_invoice_button = tkinter.Button(frame, text="GENERAR RECIBOS")
    gen_invoice_button.config(width=20, height=3, fg='green', font=('Helvetica', 16))
    gen_invoice_button.grid(row=16, column=2, sticky="news", padx=20, pady=10)


    window.mainloop()


if __name__ == '__main__':
    main()

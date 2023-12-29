#!/usr/bin/env python

import widget_gen
import invoice_gen
from tkinter import messagebox


def main():

    entries = widget_gen.run_widget()
    invoice_gen.make_invoice(entries)
    # Close the window
    messagebox.showinfo("GENERADOR DE RECIBOS", "GENERACION COMPLETADA")


if __name__ == '__main__':
    main()

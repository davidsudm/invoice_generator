#!/usr/bin/env python

import widget_gen
from tkinter import messagebox
import babel.numbers
import matplotlib.backends.backend_pdf


def main():

    widget_gen.run_widget()
    messagebox.showinfo("GENERADOR DE RECIBOS", "PROGRAMA FINALIZADO")


if __name__ == '__main__':
    main()

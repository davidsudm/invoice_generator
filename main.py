#!/usr/bin/env python

import widget_gen
from tkinter import messagebox


def main():

    widget_gen.run_widget()
    messagebox.showinfo("GENERADOR DE RECIBOS", "PROGRAMA FINALIZADO")


if __name__ == '__main__':
    main()

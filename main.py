from tkinter import *
from tkinter import ttk
from yahoo_fin.stock_info import *
import re
import ftplib
from pygal import *

def calculate(*args):
    try:
        value = symbol.get().upper()
        sdate = start_date.get()
        edate = end_date.get()
        #data = get_data(value, start_date=sdate, end_date=edate)
        data = get_data('FB', start_date='01/02/2018', end_date='01/10/2018')["close"].round(2)
        for y in data:
            print(y)
        result.set(data)
    except ValueError:
        result.set("Revise los datos ingresados")
        pass


window = Tk()
window.title("Valorización de opciones")

mainframe = ttk.Frame(window, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

symbol = StringVar()
interest = IntVar()
risk = IntVar()
start_date = StringVar()
end_date = StringVar()
result = StringVar()

symbol_entry = ttk.Entry(mainframe, width=13, textvariable=symbol)
symbol_entry.grid(column=2, row=1, sticky=(W, E))

interest_entry = ttk.Entry(mainframe, width=13, textvariable=interest)
interest_entry.grid(column=2, row=2, sticky=(W, E))

start_date_entry = ttk.Entry(mainframe, width=13, textvariable=start_date)
start_date_entry.grid(column=1, row=5, sticky=(W, E))

end_date_entry = ttk.Entry(mainframe, width=13, textvariable=end_date)
end_date_entry.grid(column=2, row=5, sticky=(W, E))

ttk.Label(mainframe, textvariable=result).grid(column=2, row=6, sticky=(W, E))
ttk.Button(mainframe, text="Calcular", command=calculate).grid(column=3, row=8, sticky=W)

ttk.Label(mainframe, text="Código empresa").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Tasa de interés").grid(column=1, row=2, sticky=W)
#ttk.Label(mainframe, text="Riesgo").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Fecha inicial").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="Fecha final").grid(column=2, row=4, sticky=W)
ttk.Label(mainframe, text="(ej: MM/DD/YYYY)").grid(column=3, row=5)
#ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Resultado").grid(column=1, row=6, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=20, pady=5)

symbol_entry.focus()
window.bind('<Return>', calculate)

window.mainloop()
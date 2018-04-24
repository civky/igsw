from tkinter import *
from tkinter import ttk
from yahoo_fin.stock_info import *
from datetime import timedelta, date
import re, socket
from pygal import *
from pandas import *
#from rpy2.robjects.packages import importr
#import rpy2.robjects as ro
#import pandas.rpy.common as com

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def data_cost():

    sdate = start_date.get().split('/')
    edate = end_date.get().split('/')
    i_date = date(int(sdate[2]), int(sdate[0]), int(sdate[1]))
    f_date = date(int(edate[2]), int(edate[0]), int(edate[1]))
    costs = []

    while True:
        end = i_date + timedelta(days=59)

        if end < f_date:
            #costs.append(get_data(symbol.get().upper(), start_date=i_date, end_date=end)["close"].round(2))
            for y in get_data(symbol.get().upper(), start_date=i_date, end_date=end)["close"].round(2):
                costs.append(y)
            #print('1' + str(costs))
            i_date = end
            pass

        elif end > f_date and i_date != f_date:
            #costs.append(get_data(symbol.get().upper(), start_date=i_date, end_date=f_date)["close"].data.round(2))
            for y in get_data(symbol.get().upper(), start_date=i_date, end_date=f_date)["close"].round(2):
                costs.append(y)
            #print('2' + str(costs))
            break

        elif end == f_date:
            break



def calculate(*args):
    try:

        inter = float(interest.get())
        result.set(data_cost())

    except ValueError:
        result.set("Revise los datos ingresados")
        pass

window = Tk()
window.title("Valorización de opciones sobre acciones")

mainframe = ttk.Frame(window, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

symbol = StringVar()
interest = StringVar()
risk = IntVar()
t_madurez = IntVar()
start_date = StringVar()
end_date = StringVar()
result = StringVar()

symbol_entry = ttk.Entry(mainframe, width=13, textvariable=symbol)
symbol_entry.grid(column=2, row=2, sticky=(W, E))

interest_entry = ttk.Entry(mainframe, width=13, textvariable=interest)
interest_entry.grid(column=2, row=1, sticky=(W, E))

t_madurez_entry = ttk.Entry(mainframe, width=13, textvariable=t_madurez)
t_madurez_entry.grid(column=4, row=1, sticky=(W,E))

start_date_entry = ttk.Entry(mainframe, width=13, textvariable=start_date)
start_date_entry.grid(column=1, row=5, sticky=(W, E))

end_date_entry = ttk.Entry(mainframe, width=13, textvariable=end_date)
end_date_entry.grid(column=2, row=5, sticky=(W, E))

ttk.Label(mainframe, textvariable=result).grid(column=2, row=6, sticky=(W, E))
ttk.Button(mainframe, text="Calcular", command=calculate).grid(column=4, row=7)

ttk.Label(mainframe, text="Código empresa").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Tasa de interés").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Tiempo de madurez").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Fecha inicial").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="Fecha final").grid(column=2, row=4, sticky=W)
ttk.Label(mainframe, text="(ej: MM/DD/YYYY)").grid(column=3, row=5)
#ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Resultado").grid(column=1, row=6, sticky=W)

state = is_connected()
if state:
    ttk.Label(mainframe, text="Conectado", foreground='green').grid(column=4, row=9, sticky=E)
else:
    ttk.Label(mainframe, text="Desconectado", foreground='red').grid(column=4, row=9, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=20, pady=5)

symbol_entry.focus()
window.bind('<Return>', calculate)

window.mainloop()
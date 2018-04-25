from tkinter import *
from tkinter import ttk
from yahoo_fin.stock_info import *
from datetime import timedelta, date
import socket
import numpy as np
from pygal import *
from pandas import *
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
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
            continue

        elif end > f_date and i_date != f_date:
            #costs.append(get_data(symbol.get().upper(), start_date=i_date, end_date=f_date)["close"].data.round(2))
            for y in get_data(symbol.get().upper(), start_date=i_date, end_date=f_date)["close"].round(2):
                costs.append(y)
            #print('2' + str(costs))
            return costs

        elif end == f_date:
            return costs


def calcular_r_sub_j(x):
    r = list()  # Aqui iran los r_j
    for i in range(len(x) - 1):
        r_i = np.log(x[i + 1] / x[i])
        r.append(r_i)
    return r

def calcular_esperanza_compra(lista_xt_finales, k, N):
    #N = 1000 #Numero de simulaciones
    sum = 0
    for i in range(len(lista_xt_finales)):
        m = max(lista_xt_finales[i] - k, 0)
        sum = sum + m
    return sum/N

def calcular_esperanza_venta(lista_xt_finales, k, N):
    #N = 1000 #Numero de simulaciones
    sum = 0
    for i in range(len(lista_xt_finales)):
        m = max(k - lista_xt_finales[i], 0)
        sum = sum + m
    return sum/N

def calculate(*args):
    try:
        #Tiempo_maduracion = t_madurez.get()
        x = data_cost()
        print(x)
        r = float(interest.get())/12
        #k = sum(x)/len(x)
        # AGREGAR A INTERFAZ

        r_p = calcular_r_sub_j(x)
        sigma = np.std(r_p)

        # Ahora calculamos los x_t a futuro hasta el tiempo de maduracion T

        T = t_madurez.get() / 12  # Tiempo_maduracion esta en meses
        lista_x_simulacion = list()  # Lista donde dejare los x_t que voy simulando
        lista_x_finales = list()  # Lista donde dejare los x_T
        x_final = x[-1]  # Obtenemos el ultimo x_t de los datos obtenidos de Yahoo Finances
        n = 1000

        # Esto esta dentro de un for con la cantidad de simulaciones que queremos hacer
        for j in range(n):  # Elegi 1000, pero pueden ser mas
            dt = T / (T * 365)

            #print(T)

            for i in range(int(T * 365)):
                #epsilon = ro.r('sample(rnorm(1000, mean=0, sd=' + str(4) + '), 1)')[0]

                if i == 0:
                    epsilon = ro.r('sample(rnorm(1000, mean=0, sd=' + str(i+1) + '), 1)')[0]  # Esta linea esta en R
                    dWu = epsilon * (dt ** 0.5)
                    dXt = (r * x_final * dt) + (sigma * x_final * dWu)
                    x_t_futuro = x_final + dXt

                else:
                    epsilon = ro.r('sample(rnorm(1000, mean=0, sd=' + str(i) + '), 1)')[0]  # Esta linea esta en R
                    dWu = epsilon * (dt ** 0.5)
                    x_t_i = lista_x_simulacion[i - 1]
                    dXt = (r * x_t_i * dt) + (sigma * x_t_i * dWu)
                    x_t_futuro = x_t_i + dXt

                lista_x_simulacion.append(x_t_futuro)
                #print(str(lista_x_simulacion))

            #print('out' + str(lista_x_simulacion))
            lista_x_finales.append(lista_x_simulacion[-1])


        # Lo demas que queda hacer, es calcular la esperanza con la formula que estan en las imagenes y luego
        # multiplicarlo por e^(-r*Tiempo_maduracion)


        print('LISTAS:' + str(lista_x_finales))

        print(np.std(lista_x_finales))
        k = int(sum(lista_x_finales) / len(lista_x_finales))
        print(k)

        esp_compra = calcular_esperanza_compra(lista_x_finales, k, n)
        esp_venta = calcular_esperanza_venta(lista_x_finales, k, n)

        print(str(esp_compra) + ':::::::' + str(esp_venta))

        f_compra = esp_compra * np.exp(-r * T)
        f_venta = esp_venta * np.exp(-r * T)


        result.set('Valor al comprar: ' + str(f_compra.round(6)) + '\n' + 'Valor al vender: ' + str(f_venta.round(6)))

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
from tkinter import *
#from tkinter import ttk
from yahoo_fin.stock_info import *
from datetime import timedelta, date
import socket
from pandas import *
import rpy2.robjects as ro
import numpy as np
import pygal
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#import cairosvg
#from rpy2.robjects.packages import importr
#import pandas.rpy.common as com


class mclass:
    def __init__(self, window, lista_x_finales):
        self.window = window
        self.lista_x_finales = lista_x_finales
        self.plot()

    def plot(self):
        x = np.arange(int(min(self.lista_x_finales)), int(max(self.lista_x_finales))+2)
        #print(x)
        # v = np.array([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        #print(len(self.lista_x_finales))
        p = np.array(self.lista_x_finales)
        #print(p)

        fig = Figure(figsize=(8, 8))
        a = fig.add_subplot(111)
        #a.scatter(x,color='red')
        a.plot(p, p, color='blue')
        #a.invert_yaxis()

        a.set_title("Estimation Grid", fontsize=10)
        a.set_ylabel("Y", fontsize=10)
        a.set_xlabel("X", fontsize=10)

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().grid(column=4, row=1)
        canvas.draw()

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
    return get_data(symbol.get().upper(), start_date=i_date, end_date=f_date)["close"].round(2)

    '''while True:
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
    '''


def calcular_r_sub_j(x):
    r = list()  # Aqui iran los r_j
    for i in range(len(x) - 1):
        r_i = np.log(x[i + 1] / x[i])
        r.append(r_i)
    return r


def calcular_esperanza_compra(lista_xt_finales, k, N):
    #N = 1000 #Numero de simulaciones
    sum = 0
    for i in range(N):
        m = max(lista_xt_finales[i] - k, 0)
        sum = sum + m
    return sum/N


def calcular_esperanza_venta(lista_xt_finales, k, N):
    #N = 1000 #Numero de simulaciones
    sum = 0
    for i in range(N):
        m = max(k - lista_xt_finales[i], 0)
        sum = sum + m
    return sum/N


def calculate(*args):
    try:
        #Tiempo_maduracion = t_madurez.get()
        x = data_cost()
        print(x)
        r = float(interest.get())/12

        r_p = calcular_r_sub_j(x)
        sigma = np.std(r_p)

        # Ahora calculamos los x_t a futuro hasta el tiempo de maduracion T

        T = t_madurez.get() / 12  # Tiempo_maduracion esta en meses
        lista_x_simulacion = list()  # Lista donde dejare los x_t que voy simulando
        lista_x_finales = list()  # Lista donde dejare los x_T
        x_final = x[-1]  # Obtenemos el ultimo x_t de los datos obtenidos de Yahoo Finances
        n = int(n_iter.get()) #Número de iteraciones

        # Esto esta dentro de un for con la cantidad de simulaciones que queremos hacer
        for j in range(n):
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

        #print('LISTAS:' + str(lista_x_finales))

        #print(np.std(lista_x_finales))
        k = int(sum(lista_x_finales) / len(lista_x_finales))  # promedio de valores simulados
        #print(k)

        esp_compra = calcular_esperanza_compra(lista_x_finales, k, n)
        esp_venta = calcular_esperanza_venta(lista_x_finales, k, n)

        print(str(esp_compra) + ':::::::' + str(esp_venta))

        #resultados = [esp_compra * np.exp(-r * T), esp_venta * np.exp(-r * T) ]
        f_compra = esp_compra * np.exp(-r * T)
        f_venta = esp_venta * np.exp(-r * T)
        result.set('Valor al comprar: ' + str(f_compra.round(6)) + '\n' + 'Valor al vender: ' + str(f_venta.round(6)))

        start = mclass(window, lista_x_finales)


    except ValueError:
        result.set("Revise los datos ingresados")
        pass


window = Tk()
window.title("Valorización de opciones sobre acciones")
window.configure(bg="#2E3037")

mainframe = Frame(window, bg="#2E3037")
# padding="12 12 12 12", 
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

symbol = StringVar()
interest = StringVar()
risk = IntVar()
t_madurez = IntVar()
n_iter = IntVar()
start_date = StringVar()
end_date = StringVar()
result = StringVar()

symbol_entry = Entry(mainframe, width=13, textvariable=symbol)
symbol_entry.grid(column=2, row=2, sticky=(W, E))

interest_entry = Entry(mainframe, width=13, textvariable=interest)
interest_entry.grid(column=2, row=1, sticky=(W, E))

t_madurez_entry = Entry(mainframe, width=13, textvariable=t_madurez)
t_madurez_entry.grid(column=4, row=1, sticky=(W,E))

n_iter_entry = Entry(mainframe, width=13, textvariable=n_iter)
n_iter_entry.grid(column=4, row=2, sticky=(W,E))

start_date_entry = Entry(mainframe, width=13, textvariable=start_date)
start_date_entry.grid(column=1, row=5, sticky=(W, E))

end_date_entry = Entry(mainframe, width=13, textvariable=end_date)
end_date_entry.grid(column=2, row=5, sticky=(W, E))

Label(mainframe, textvariable=result).grid(column=2, row=6, sticky=(W, E))

Button(mainframe, text="Calcular", command=calculate, bg="#39C0BA", fg="white").grid(column=4, row=7)

Label(mainframe, text="Código empresa", bg="#2E3037", fg="white").grid(column=1, row=2, sticky=W)
Label(mainframe, text="Tasa de interés", bg="#2E3037", fg="white").grid(column=1, row=1, sticky=W)
Label(mainframe, text="Tiempo de madurez", bg="#2E3037", fg="white").grid(column=3, row=1, sticky=W)
Label(mainframe, text="Número de iteraciones", bg="#2E3037", fg="white").grid(column=3, row=2, sticky=W)
Label(mainframe, text="Fecha inicial", bg="#2E3037", fg="white").grid(column=1, row=4, sticky=W)
Label(mainframe, text="Fecha final", bg="#2E3037", fg="white").grid(column=2, row=4, sticky=W)
Label(mainframe, text="(ej: MM/DD/YYYY)", bg="#2E3037", fg="white").grid(column=3, row=5)
#Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
Label(mainframe, text="Resultado", bg="#2E3037", fg="white").grid(column=1, row=6, sticky=W)

state = is_connected()
if state:
    Label(mainframe, text="Conectado", foreground='green', bg="#2E3037").grid(column=4, row=9, sticky=E)
else:
    Label(mainframe, text="Desconectado", foreground='red', bg="#2E3037").grid(column=4, row=9, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=20, pady=5)

symbol_entry.focus()
#result.set('Valor al comprar: ' + str(results[0].round(6)) + '\n' + 'Valor al vender: ' + str(results[1].round(6)))
window.bind('<Return>', calculate)
window.mainloop()

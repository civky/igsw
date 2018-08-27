from tkinter import *
import bcrypt as bcrypt
from tkinter import filedialog
from yahoo_fin.stock_info import *
from datetime import date
import csv
import rpy2.robjects as ro
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

LARGE_FONT = ("Verdana", 12)
ARGUS = list()


def acceso(pasw):

    password = b'$2b$14$lfs4Pa3EkXMB2IOer7WmOeZzzytJYczWw5uU8fYZjrjVwJkgupwRq'
    to_check = str(pasw)
    if bcrypt.checkpw(to_check.encode('utf8'), password):
        return True
    else:
        return False


class Valorizacion_opts_app(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        self.title('Valorizador de opciones sobre acciones')
        #container.pack(side="top", fill="both", expand=True)
        container.grid(column=0, row=0)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        #for F in (StartPage, PageOne, PageTwo):
        for F in (StartPage, PageOne):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Para acceder ingrese su contraseña", font=LARGE_FONT)
        label.grid(column=1, row=1, sticky=(N,E))

        pasw = StringVar()
        pasw_entry = Entry(self, width=40, textvariable=pasw, show="*")
        pasw_entry.grid(column=1, row=2)

        psw_wrong_label = Label(self, text="Contraseña incorrecta")

        button = Button(self, text="Acceder",
                        command=lambda: controller.show_frame(PageOne) if acceso(pasw.get()) is True else psw_wrong_label.grid(column=1, row=3))
        button.grid(column=2, row=2)


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.configure(self, bg="#333333")

        self.controller = controller
        self.symbol = StringVar()
        self.interest = StringVar()
        self.risk = IntVar()
        self.t_madurez = IntVar()
        self.n_iter = IntVar()
        self.m_iter = IntVar()
        self.start_date = StringVar()
        self.end_date = StringVar()
        self.result = StringVar()
        self.rb = IntVar()
        self.file_csv = StringVar()
        self.col_date = IntVar()
        self.col_data = IntVar()

        self.rb.set(1)

        R1 = Radiobutton(self, bg="#333333", fg="white", text="Yahoo finances",
                         variable=self.rb, value=1, font=('Impact', '13'), command=self.sel_rb).grid(column=1, row=2, sticky=W,
                                                                                           columnspan=3)

        R2 = Radiobutton(self, bg="#333333", fg="white", text="Subir archivo",
                         variable=self.rb, value=2, font=('Impact', '13'), command=self.sel_rb).grid(column=1, row=7, sticky=W,
                                                                                           columnspan=3)

        symbol_entry = Entry(self, width=13, textvariable=self.symbol.get())
        symbol_entry.grid(column=2, row=3, sticky=(W, E))

        start_date_entry = Entry(self, width=13, textvariable=self.start_date)
        start_date_entry.grid(column=2, row=4, sticky=(W, E))

        end_date_entry = Entry(self, width=13, textvariable=self.end_date)
        end_date_entry.grid(column=2, row=5, sticky=(W, E))

        col_date_entry = Entry(self, width=13, textvariable=self.col_date)
        col_date_entry.grid(column=2, row=9, sticky=(W, E))

        col_data_entry = Entry(self, width=13, textvariable=self.col_data)
        col_data_entry.grid(column=2, row=10, sticky=(W, E))

        Label(self, textvariable=self.result, bg="#333333", fg="white").grid(column=3, row=9, sticky=(W, E))
        Label(self, textvariable=self.file_csv).grid(column=1, row=8, sticky=(W, E))

        interest_entry = Entry(self, width=13, textvariable=self.interest)
        interest_entry.grid(column=4, row=2, sticky=(W, E))

        t_madurez_entry = Entry(self, width=13, textvariable=self.t_madurez)
        t_madurez_entry.grid(column=4, row=3, sticky=(W, E))

        n_iter_entry = Entry(self, width=13, textvariable=self.n_iter)
        n_iter_entry.grid(column=4, row=4, sticky=(W, E))

        title1 = Label(self, text="Obtención de datos", bg="#333333", fg="white", font=('Impact', '20')).grid(
            column=1, row=1, sticky=W)
        title2 = Label(self, text="Ingresar parámetros", bg="#333333", fg="white", font=('Impact', '20')).grid(
            column=3, row=1, sticky=W)

        Label(self, text="Código empresa", bg="#333333", fg="white").grid(column=1, row=3, sticky=W)
        Label(self, text="Fecha inicial", bg="#333333", fg="white").grid(column=1, row=4, sticky=W)
        Label(self, text="Fecha final", bg="#333333", fg="white").grid(column=1, row=5, sticky=W)
        Label(self, text="(ej: MM/DD/YYYY)", bg="#333333", fg="white").grid(column=2, row=6)

        Button(self, text="Elegir archivo", command=self.open_file).grid(column=2, row=8, sticky=W)
        Label(self, text="Ingresar n° de columna fecha", bg="#333333", fg="white").grid(column=1, row=9, sticky=W)
        Label(self, text="Ingresar n° de columna datos", bg="#333333", fg="white").grid(column=1, row=10, sticky=W)

        Label(self, text="Tasa de interés", bg="#333333", fg="white").grid(column=3, row=2, sticky=W)
        Label(self, text="Tiempo de madurez", bg="#333333", fg="white").grid(column=3, row=3, sticky=W)
        Label(self, text="Número de iteraciones", bg="#333333", fg="white").grid(column=3, row=4, sticky=W)
        Label(self, text="Número de iteraciones del tiempo", bg="#333333", fg="white").grid(column=3, row=8, sticky=W)
        Label(self, text="Resultado", bg="#333333", fg="white", font=('Impact', '20')).grid(column=3, row=10, sticky=W)

        Label(self, text="---", bg="#333333", fg="#333333").grid(column=1, row=11, sticky=W)

        btn_calcular = Button(self, text="Calcular", command=self.calculate, bg="#39C0BA", fg="white").grid(column=4, row=7)
        symbol_entry.focus()
        self.bind('<Return>', self.calculate)

        '''
        button2 = Button(self, text="Calcular",
                         command=lambda: controller.show_frame(PageTwo))
        button2.pack() '''


    def open_file(self):
        new_file = filedialog.askopenfilenames(parent=self, initialdir='./', initialfile='',
                                          filetypes=[("CSV", "*.csv"), ("All files", "*")])
        self.file_csv.set(new_file[0])
        return new_file


    def sel_rb(self):
        selection = "You selected the option " + str(self.rb.get())
        #Label.config(text=selection)
        print(selection)


    def data_cost(self):

        sdate = self.start_date.get().split('/')
        edate = self.end_date.get().split('/')
        i_date = date(int(sdate[2]), int(sdate[0]), int(sdate[1]))
        f_date = date(int(edate[2]), int(edate[0]), int(edate[1]))
        return get_data(self.symbol.get().upper(), start_date=i_date, end_date=f_date)["close"].round(2)


    def calcular_r_sub_j(self, x):
        r = list()  # Aqui iran los r_j
        for i in range(len(x) - 1):
            r_i = np.log(x[i + 1] / x[i])
            r.append(r_i)
        return r


    def calcular_esperanza_compra(self, lista_xt_finales, k, N):
        #N = 1000 #Numero de simulaciones
        sum = 0
        for i in range(N):
            m = max(lista_xt_finales[i] - k, 0)
            sum = sum + m
        return sum/N


    def calcular_esperanza_venta(self, lista_xt_finales, k, N):
        #N = 1000 #Numero de simulaciones
        sum = 0
        for i in range(N):
            m = max(k - lista_xt_finales[i], 0)
            sum = sum + m
        return sum/N


    def calculate(self):
        try:
            x = list()
            #Tiempo_maduracion = t_madurez.get()
            if self.rb.get() == 1:
                x = self.data_cost()

            elif self.rb.get() == 2:
                with open(self.file_csv.get(), 'r') as csv_upload:
                    csv_reader = csv.reader(csv_upload)
                    next(csv_reader)
                    for line in csv_reader:
                        #print(line)
                        x.append(float(line[self.col_data.get()]))

                #print('en proceso')
                del x[0]

            #print(x)
            r = float(self.interest.get())/12

            r_p = self.calcular_r_sub_j(x)
            sigma = np.std(r_p)

            # Ahora calculamos los x_t a futuro hasta el tiempo de maduracion T

            T = self.t_madurez.get() / 12  # Tiempo_maduracion esta en meses
            lista_x_simulacion = list()  # Lista donde dejare los x_t que voy simulando
            lista_x_finales = list()  # Lista donde dejare los x_T
            x_final = x[-1]  # Obtenemos el ultimo x_t de los datos obtenidos de Yahoo Finances
            n = int(self.n_iter.get()) #Número de iteraciones

            # Esto esta dentro de un for con la cantidad de simulaciones que queremos hacer
            for j in range(n):
                #dt = T / (T * 365)
                dt = (T-0)/n

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

            esp_compra = self.calcular_esperanza_compra(lista_x_finales, k, n)
            esp_venta = self.calcular_esperanza_venta(lista_x_finales, k, n)

            #print(str(esp_compra) + ':::::::' + str(esp_venta))

            #resultados = [esp_compra * np.exp(-r * T), esp_venta * np.exp(-r * T) ]
            f_compra = (esp_compra * np.exp(-r * T)).round(6)
            f_venta = (esp_venta * np.exp(-r * T)).round(6)

            #lambda: controller.show_frame(PageOne) if acceso(pasw.get()) is True else psw_wrong_label.grid(column=2, row=2))

            global ARGUS
            ARGUS = (lista_x_finales, f_compra, f_venta, n, T)
            #print('UNO')

            #self.controller.show_frame(PageTwo)

            frame2 = PageTwo(self.master, self.controller)
            frame2.grid(row=0, column=0, sticky="nsew")
            frame2.tkraise()

        except ValueError:
            self.result.set("Revise los datos ingresados")
            pass


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.plot()
        global ARGUS
        print(ARGUS[1])
        Label(self, text='Precio de venta: ' + str(ARGUS[1]), bg="#333333", fg="white").grid(column=1, row=2,
                                                                                                sticky=W)
        Label(self, text='Precio de compra: ' + str(ARGUS[2]), bg="#333333", fg="white").grid(column=1, row=3,
                                                                                                 sticky=W)
        button_page_one = Button(self, text="Volver", command=lambda: controller.show_frame(PageOne))
        button_page_one.grid(row=2, column=1, sticky=E)

        self.plot()
    
    def plot(self):

        global ARGUS
        #print('DOS')
        if len(ARGUS) != 0:
            lista_x_finales = ARGUS[0]
            N = ARGUS[3]
            T = ARGUS[4]

            # v = np.array([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
            p = np.array(lista_x_finales)  # precios
            p = np.log(p)

            fig = Figure(figsize=(7, 6), linewidth=1)
            a = fig.add_subplot(111)
            a.plot((T / N) * np.arange(N), p, color='blue')
            a.set_title("Trayectorias para el precio de la acción", fontsize=10)
            a.set_ylabel('Precio', fontsize=10)
            a.set_xlabel('Tiempo', fontsize=10)

            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().grid(column=1, row=1)
            canvas.draw()

app = Valorizacion_opts_app()
app.mainloop()

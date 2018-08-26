

class mclass:
    def __init__(self, window, lista_x_finales, N, T):
        self.window = window
        self.lista_x_finales = lista_x_finales
        self.N = N
        self.T = T
        self.plot()

    def plot(self):
        #print(self.lista_x_finales)
        #x = np.arange(int(min(self.lista_x_finales)), int(max(self.lista_x_finales))+2)
        #print(x)
        # v = np.array([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        #print(len(self.lista_x_finales))
        p = np.array(self.lista_x_finales) #precios
        p = np.log(p)
        #print(self.T)
        #print(self.N)

        fig = Figure(figsize=(7,6), linewidth=1)
        a = fig.add_subplot(111)
        #a.scatter(x,color='red')
        #print((T/N)*np.arange(N))
        a.plot((self.T/self.N)*np.arange(self.N), p, color='blue')
        #a.invert_yaxis()

        a.set_title("Trayectorias para el precio de la acción", fontsize=10)
        a.set_ylabel('Precio', fontsize=10)
        a.set_xlabel('Tiempo', fontsize=10)

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().grid(column=6, row=0, sticky=(N, W))
        canvas.draw()
        ''' 
        line_chart = pygal.Line()
        line_chart.title = 'Trayectorias para el precio de la acción'
        line_chart.x_labels = (self.T/self.N)*np.arange(self.N)
        line_chart.add('Precios', p)
        line_chart.render_to_file('/tmp/bar_chart.svg')
        '''



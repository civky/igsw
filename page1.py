# Multi-frame tkinter application v2.2
import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage, 'yay')

    def switch_frame(self, frame_class, data):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, data)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)

        start_label = tk.Label(self, text="This is the start page")
        page_1_button = tk.Button(self, text="Continuar",
                                  command=lambda: master.switch_frame(PageOne(master, 'gg')))
        page_2_button = tk.Button(self, text="Open page two",
                                  command=lambda: master.switch_frame(PageTwo))
        start_label.pack(side="top", fill="x", pady=10)
        page_1_button.pack()
        page_2_button.pack()


class PageOne(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)

        page_1_label = tk.Label(self, text="This is page one" + data)
        start_button = tk.Button(self, text="Return to start page",
                                 command=lambda: master.switch_frame(StartPage))
        page_1_label.pack(side="top", fill="x", pady=10)
        start_button.pack()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        page_2_label = tk.Label(self, text="This is page two")
        start_button = tk.Button(self, text="Return to start page",
                                 command=lambda: master.switch_frame(StartPage))
        page_2_label.pack(side="top", fill="x", pady=10)
        start_button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
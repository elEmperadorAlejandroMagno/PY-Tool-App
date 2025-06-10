import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import time
from translations.translations import get_translations as translations
from apps.timer import CubeScrambler, TimerLogic

class TimerAppGUI:
    def __init__(self, lang="en"):
        self.translations = translations.get(lang, translations["en"])["timer"]
        self.logic = TimerLogic()
        self.press_time = None
        self.running = False
        self.current_algorithm = CubeScrambler.generate_algorithm("3x3")

        self.root = tk.Tk()
        self.root.title(self.translations['title'])

        self.label = tk.Label(self.root, text=self.translations['press_space'], font=("Arial", 12))
        self.label.pack(pady=20)

        self.cube_sizes = [cube["size"] for cube in CubeScrambler.cubes]
        self.selected_cube = tk.StringVar(value="3x3")
        self.cube_menu = tk.OptionMenu(self.root, self.selected_cube, *self.cube_sizes, command=self.on_cube_change)
        self.cube_menu.pack(pady=5)

        self.button = tk.Button(self.root, text=self.translations['generate_algorithm'], command=self.show_algorithm)
        self.button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 10), wraplength=300)
        self.result_label.pack(pady=10)

        self.best_time_label = tk.Label(self.root, text=f"{self.translations['best_time']}: {self.translations['no_record']}", font=("Arial", 10))
        self.best_time_label.pack(pady=10)

        self.worst_time_label = tk.Label(self.root, text=f"{self.translations['worst_time']}: {self.translations['no_record']}", font=("Arial", 10))
        self.worst_time_label.pack(pady=10)

        self.average_time_label = tk.Label(self.root, text=f"{self.translations['average_time']}: --", font=("Arial", 10))
        self.average_time_label.pack(pady=10)

        self.times_tree = ttk.Treeview(self.root, columns=("n", "time"), show="headings", height=7)
        self.times_tree.heading("n", text="#")
        self.times_tree.heading("time", text="")
        self.times_tree.column("n", width=30, anchor="center")
        self.times_tree.column("time", width=80, anchor="center")
        self.times_tree.pack(pady=10)

        self.times_tree.bind("<Double-1>", self.on_time_double_click)

        self.root.bind_all("<KeyPress>", self.on_key_press)
        self.show_algorithm()

    def add_time(self, elapsed, algorithm):
        self.logic.add_time(elapsed, algorithm)

    def actualizar_etiquetas(self):
        t = self.translations
        times = self.logic._times_dict
        if times:
            # Limpiar la tabla
            for row in self.times_tree.get_children():
                self.times_tree.delete(row)
            # Insertar nuevos datos
            for item in times.values():
                self.times_tree.insert("", "end",iid=str(item["id"]), values=(item["id"], f"{item['time']:.2f}s"))

                self.average_time_label.config(text=f"{t['average_time']}: {self.logic.average_time:.2f} s")
        else:
            self.times_tree.delete(*self.times_tree.get_children())
            self.average_time_label.config(text=f"{t['average_time']}: --")
        if self.logic.best_time is not None:
            self.best_time_label.config(text=f"{t['best_time']}: {self.logic.best_time:.2f} s")
        if self.logic.worst_time is not None:
            self.worst_time_label.config(text=f"{t['worst_time']}: {self.logic.worst_time:.2f} s")

    def on_cube_change(self, *args):
        self.show_algorithm()

    def on_key_press(self, event):
        t = self.translations
        if event.keysym == "space":
            if not self.running:
                self.press_time = time.time()
                self.running = True
                self.update_timer()
            else:
                elapsed = time.time() - self.press_time
                self.label.config(text=f"{elapsed:.2f}")
                self.add_time(elapsed, self.current_algorithm)
                self.running = False
                self.actualizar_etiquetas()
                if elapsed == self.logic.best_time:
                    messagebox.showinfo(t["best_time"], f"¡{t['best_time']}: {self.logic.best_time:.2f} segundos!")
                self.show_algorithm()

    def show_algorithm(self):
        cube_type = self.selected_cube.get().strip()
        self.current_algorithm = CubeScrambler.generate_algorithm(cube_type)
        self.result_label.config(text=f"{self.translations['generate_algorithm']}: {self.current_algorithm}")

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.press_time
            self.label.config(text=f"{elapsed:.2f} s")
            self.root.after(100, self.update_timer)

    def on_time_double_click(self, event):
        item_id = self.times_tree.focus()
        if not item_id:
            return
        time_id = int(item_id)
        time_data = next((item for item in self.logic._times_dict.values() if item["id"] == time_id), None)
        if not time_data:
            messagebox.showerror("Error", "No se encontró el tiempo seleccionado.")
            return

        # Crear ventana personalizada
        win = tk.Toplevel(self.root)
        win.title("Detalle del tiempo")
        win.geometry("400x250")
        tk.Label(win, text=f"Tiempo: {time_data['time']:.2f}s", font=("Arial", 12)).pack(pady=10)
        tk.Label(win, text="Algoritmo:", font=("Arial", 10, "bold")).pack()
        tk.Message(win, text=time_data['algorithm'], width=380).pack(pady=5)

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=15)

        def sumar_dos_segundos():
            self.logic._times_dict[time_id]["time"] += 2
            self.actualizar_etiquetas()
            btn_sumar.config(state="disabled")

        def borrar():
            self.logic.delete_time(time_id)
            self.actualizar_etiquetas()
            win.destroy()

        btn_sumar = tk.Button(btn_frame, text="Sumar +2s", command=sumar_dos_segundos, fg="white", bg="blue")
        btn_sumar.pack(side="left", padx=10)
        tk.Button(btn_frame, text="Borrar", command=borrar, fg="white", bg="red").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cerrar", command=win.destroy).pack(side="left", padx=10)
        

    def run(self):
        self.root.mainloop()
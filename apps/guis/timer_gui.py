import tkinter as tk
import tkinter.messagebox as messagebox
import time
from translations.translations import get_translations as translations
from apps.timer import CubeScrambler, TimerLogic

class TimerAppGUI:
    def __init__(self, lang="en"):
        self.translations = translations.get(lang, translations["en"])["timer"]
        self.logic = TimerLogic()
        self.press_time = None
        self.running = False

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

        self.times_label = tk.Label(self.root, text=f"{self.translations['recorded_times']}: []", font=("Arial", 10))
        self.times_label.pack(pady=10)

        self.root.bind_all("<KeyPress>", self.on_key_press)
        self.show_algorithm()

    def add_time(self, elapsed):
        self.logic.add_time(elapsed)

    def actualizar_etiquetas(self):
        t = self.translations
        times = self.logic.times_list
        if times:
            self.times_label.config(text=f"{t['recorded_times']}: {[f'{tiempo:.2f}' for tiempo in times]}")
            self.average_time_label.config(text=f"{t['average_time']}: {self.logic.average_time:.2f} s")
        else:
            self.times_label.config(text=f"{t['recorded_times']}: []")
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
                self.add_time(elapsed)
                self.running = False
                self.actualizar_etiquetas()
                if elapsed == self.logic.best_time:
                    messagebox.showinfo(t["best_time"], f"¡{t['best_time']}: {self.logic.best_time:.2f} segundos!")
                self.show_algorithm()

    def show_algorithm(self):
        cube_type = self.selected_cube.get().strip()
        algorithm = CubeScrambler.generate_algorithm(cube_type)
        self.result_label.config(text=f"{self.translations['generate_algorithm']}: {algorithm}")

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.press_time
            self.label.config(text=f"{elapsed:.2f} s")
            self.root.after(100, self.update_timer)

    def run(self):
        self.root.mainloop()
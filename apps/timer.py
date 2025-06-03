import tkinter as tk
import tkinter.messagebox as messagebox
import random
import time
from translations.translations import get_translations as translations

class CubeScrambler:
    cubes = [
        {
            "size": "3x3",
            "moves": ["U", "U-", "U2", "D", "D-", "D2", "L", "L-", "L2", "R", "R-", "R2", "F", "F-", "F2", "B", "B-", "B2"],
            "num_moves": 20
        },
        {
            "size": "2x2",
            "moves": ["U", "U-", "U2", "D", "D-", "D2", "L", "L-", "L2", "R", "R-", "R2", "F", "F-", "F2", "B", "B-", "B2"],
            "num_moves": 11
        },
        {
            "size": "4x4",
            "moves": ["U", "U-", "U2", "Uw", "Uw-", "Uw2", "D", "D-", "D2", "Dw", "Dw-", "Dw2", "L", "L-", "L2", "Rw", "Rw-", "Rw2", "R", "R-", "R2", "F", "F-", "F2", "B", "B-", "B2"],
            "num_moves": 40
        }
    ]

    @classmethod
    def get_cube_info(cls, size):
        for cube in cls.cubes:
            if cube["size"] == size:
                return cube["moves"], cube["num_moves"]
        raise ValueError(f"Error: Tipo de cubo {size} no encontrado")

    @classmethod
    def generate_algorithm(cls, cube_type):
        try:
            moves, num_moves = cls.get_cube_info(cube_type)
            algorithm = []
            for _ in range(num_moves):
                move = None
                while (move is None) or (algorithm and move[0] == algorithm[-1][0]):
                    move = random.choice(moves)
                algorithm.append(move)
            return " ".join(algorithm)
        except ValueError:
            return "Error al generar mezcla"

class TimerApp:
    def __init__(self, lang="en"):
        self.translations = translations.get(lang, translations["en"])["timer"]
        self.press_time = None
        self.running = False
        self._times_list = []
        self._best_time = None

        self.root = tk.Tk()
        self.root.title(self.translations['title'])

        self.label = tk.Label(self.root, text=self.translations['press_space'], font=("Arial", 12))
        self.label.pack(pady=20)

        self.entry_label = tk.Label(self.root, text=self.translations['cube_size'], font=("Arial", 10))
        self.entry_label.pack(pady=10)
        self.cube_entry = tk.Entry(self.root)
        self.cube_entry.pack(pady=5)

        self.button = tk.Button(self.root, text=self.translations['generate_algorithm'], command=self.show_algorithm)
        self.button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 10), wraplength=300)
        self.result_label.pack(pady=10)

        self.best_time_label = tk.Label(self.root, text=f"{self.translations['best_time']}: {self.translations['no_record']}", font=("Arial", 10))
        self.best_time_label.pack(pady=10)

        self.average_time_label = tk.Label(self.root, text=f"{self.translations['average_time']}: --", font=("Arial", 10))
        self.average_time_label.pack(pady=10)

        self.times_label = tk.Label(self.root, text=f"{self.translations['recorded_times']}: []", font=("Arial", 10))
        self.times_label.pack(pady=10)

        self.root.bind_all("<KeyPress>", self.on_key_press)

    @property
    def best_time(self):
        return self._best_time

    @best_time.setter
    def best_time(self, value):
        if value is not None and value < 0:
            raise ValueError("El mejor tiempo no puede ser negativo.")
        self._best_time = value

    @property
    def times_list(self):
        return self._times_list.copy()  # Previene modificaciones directas

    def add_time(self, elapsed):
        if elapsed < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        self._times_list.append(elapsed)
        if self._best_time is None or elapsed < self._best_time:
            self.best_time = elapsed

    def actualizar_etiquetas(self):
        t = self.translations
        if self._times_list:
            self.times_label.config(text=f"{t['recorded_times']}: {[f'{tiempo:.2f}' for tiempo in self._times_list]}")
            average = sum(self._times_list) / len(self._times_list)
            self.average_time_label.config(text=f"{t['average_time']}: {average:.2f} segundos")
        else:
            self.times_label.config(text=f"{t['recorded_times']}: []")
            self.average_time_label.config(text=f"{t['average_time']}: --")
        if self._best_time is not None:
            self.best_time_label.config(text=f"{t['best_time']}: {self._best_time:.2f} segundos")
        else:
            self.best_time_label.config(text=f"{t['best_time']}: {t['no_record']}")

    def on_key_press(self, event):
        t = self.translations
        if event.keysym == "space":
            if not self.running:
                self.press_time = time.time()
                self.label.config(text=t["press_space"])
                self.running = True
            else:
                elapsed = time.time() - self.press_time
                self.label.config(text=f"{t['best_time']}: {elapsed:.2f} segundos")
                self.add_time(elapsed)
                if self.best_time == elapsed:
                    messagebox.showinfo(t["best_time"], f"¡{t['best_time']}: {self.best_time:.2f} segundos!")
                self.running = False
                self.actualizar_etiquetas()

    def show_algorithm(self):
        cube_type = self.cube_entry.get().strip()
        algorithm = CubeScrambler.generate_algorithm(cube_type)
        self.result_label.config(text=f"{self.translations['generate_algorithm']}: {algorithm}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimerApp(lang="en")
    app.run()

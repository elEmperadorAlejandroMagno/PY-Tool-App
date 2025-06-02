import tkinter as tk
import tkinter.messagebox as messagebox
import random
import time
from translations.translations import get_translations as translations
t =  translations["en"]["timer"]

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

def generate_algorithm(cube_type):
    try:
        tup = get_cube_info(cube_type)
        algorithm = []
        for _ in range(tup[1]):
            move = None
            while (move is None) or (algorithm) and (move[0] == algorithm[-1][0]):
                move = random.choice(tup[0])
            algorithm.append(move)
        return " ".join(algorithm)
    except ValueError:
        return "Error al generar mezcla"

def get_cube_info(size):
    for cube in cubes:
        if cube["size"] == size:
            return (cube["moves"], cube["num_moves"])
    raise ValueError(f"Error: Tipo de cubo {size} no encontrado")

# Variables globales
press_time = None
running = False
times_list = []
best_time = None

def actualizar_etiquetas():
    if times_list:
        times_label.config(text=f"{t['recorded_times']}: {[f'{tiempo:.2f}' for tiempo in times_list]}")
        average = sum(times_list) / len(times_list)
        average_time_label.config(text=f"{t['average_time']}: {average:.2f} segundos")
    else:
        times_label.config(text=f"{t['recorded_times']}: []")
        average_time_label.config(text=f"{t['average_time']}: --")
    if best_time is not None:
        best_time_label.config(text=f"{t['best_time']}: {best_time:.2f} segundos")
    else:
        best_time_label.config(text=f"{t['best_time']}: {t['no_record']}")

def on_key_press(event):
    global press_time, running, times_list, best_time
    if event.keysym == "space":
        if not running:
            press_time = time.time()
            label.config(text=t["press_space"])
            running = True
        else:
            elapsed = time.time() - press_time
            label.config(text=f"{t['best_time']}: {elapsed:.2f} segundos")
            times_list.append(elapsed)
            if best_time is None or elapsed < best_time:
                best_time = elapsed
                messagebox.showinfo(t["best_time"], f"¡{t['best_time']}: {best_time:.2f} segundos!")
            running = False
            actualizar_etiquetas()

# Botón para generar algoritmo
def show_algorithm():
    cube_type = cube_entry.get().strip()
    algorithm = generate_algorithm(cube_type)
    result_label.config(text=f"{t['generate_algorithm']}: {algorithm}")

def main(lang):
    global t, label, cube_entry, result_label, best_time_label, average_time_label, times_label
    t = translations.get(lang, translations["en"])["timer"]

    root = tk.Tk()

    root.title(f"{t['title']}")
    button = tk.Button(root, text=t["generate_algorithm"], command=show_algorithm)
    button.pack(pady=10)
    # Etiqueta para mostrar el cronómetro
    label = tk.Label(root, text=f"{t['press_space']}", font=("Arial", 12))
    label.pack(pady=20)

    # Campo de entrada para el tamaño del cubo
    entry_label = tk.Label(root, text=f"{t['cube_size']}", font=("Arial", 10))
    entry_label.pack(pady=10)
    cube_entry = tk.Entry(root)
    cube_entry.pack(pady=5)
    # Etiqueta para mostrar el algoritmo generado
    result_label = tk.Label(root, text="", font=("Arial", 10), wraplength=300)
    result_label.pack(pady=10)
    best_time_label = tk.Label(root, text=f"{t['best_time']}: {t['no_record']}", font=("Arial", 10))
    best_time_label.pack(pady=10)
    average_time_label = tk.Label(root, text=f"{t['average_time']}: --", font=("Arial", 10))
    average_time_label.pack(pady=10)
    times_label = tk.Label(root, text=f"{t['recorded_times']}: []", font=("Arial", 10))
    times_label.pack(pady=10)

    # Vincular eventos de teclado a toda la aplicación
    root.bind_all("<KeyPress>", on_key_press)
    root.mainloop()

if __name__ == "__main__":
    main()

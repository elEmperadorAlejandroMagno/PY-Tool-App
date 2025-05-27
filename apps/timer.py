import tkinter as tk
import random
import sys
import time

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

def on_key_press(event):
    global press_time, running
    if event.keysym == "space":
        if not running:
            press_time = time.time()
            label.config(text="Cronómetro corriendo...")
            running = True
        else:
            elapsed = time.time() - press_time
            label.config(text=f"Tiempo: {elapsed:.2f} segundos")
            running = False

# Creación de la ventana
root = tk.Tk()
root.title("Cronómetro & Algoritmo")

# Etiqueta para mostrar el cronómetro
label = tk.Label(root, text="Presiona y mantén el espacio", font=("Arial", 12))
label.pack(pady=20)

# Campo de entrada para el tamaño del cubo
entry_label = tk.Label(root, text="Ingrese tamaño del cubo (Ej: 3x3):", font=("Arial", 10))
entry_label.pack(pady=10)
cube_entry = tk.Entry(root)
cube_entry.pack(pady=5)

# Botón para generar algoritmo
def show_algorithm():
    cube_type = cube_entry.get().strip()
    algorithm = generate_algorithm(cube_type)
    result_label.config(text=f"Algoritmo generado: {algorithm}")

button = tk.Button(root, text="Generar algoritmo", command=show_algorithm)
button.pack(pady=10)

# Etiqueta para mostrar el algoritmo generado
result_label = tk.Label(root, text="", font=("Arial", 10), wraplength=300)
result_label.pack(pady=10)

# Vincular eventos de teclado a toda la aplicación
root.bind_all("<KeyPress>", on_key_press)

def main():
    global label, cube_entry, result_label
    # Iniciar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    root.mainloop()

import random

class CubeScrambler:
    cubes = [
        {
            "size": "2x2",
            "moves": ["U", "U-", "U2", "D", "D-", "D2", "L", "L-", "L2", "R", "R-", "R2", "F", "F-", "F2", "B", "B-", "B2"],
            "num_moves": 11
        },
        {
            "size": "3x3",
            "moves": ["U", "U-", "U2", "D", "D-", "D2", "L", "L-", "L2", "R", "R-", "R2", "F", "F-", "F2", "B", "B-", "B2"],
            "num_moves": 20
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

class TimerLogic:
    def __init__(self):
        self._id_counter = 0
        self._times_dict = {}
        self._average_time = None
        self._best_time = None
        self._worst_time = None

    def add_time(self, elapsed, algorithm):
        if elapsed < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        self._id_counter += 1
        self._times_dict[self._id_counter] = {"id": self._id_counter, "time": elapsed, "algorithm": algorithm}

    def delete_time(self, time_id):
        try:
            self._times_dict.pop(time_id, None)
        except KeyError:
            raise ValueError(f"Tiempo con ID {time_id} no encontrado.")

    @property
    def id_counter(self):
        return self._id_counter

    @property
    def best_time(self):
        return min(self._times_dict.values(), key=lambda x: x["time"])["time"] if self._times_dict.values() else None
    
    @best_time.setter
    def best_time(self, value):
        if value < 0:
            raise ValueError("El mejor tiempo no puede ser negativo.")
        self._best_time = value

    @property
    def worst_time(self):
        return max(self._times_dict.values(), key=lambda x: x["time"])["time"] if self._times_dict.values() else None
    
    @worst_time.setter
    def worst_time(self, value):
        if value < 0:
            raise ValueError("El peor tiempo no puede ser negativo.")
        self._worst_time = value

    @property
    def average_time(self):
        return sum(x["time"] for x in self._times_dict.values()) / len(self._times_dict.values()) if self._times_dict.values() else None
    
    @average_time.setter
    def average_time(self, value):
        if value < 0:
            raise ValueError("El tiempo promedio no puede ser negativo.")
        self._average_time = value

    @property
    def times_dict(self):
        return self._times_dict.values()
    
def main(lang="en"):
    from apps.guis.timer_gui import TimerAppGUI
    app = TimerAppGUI(lang)
    app.run()

if __name__ == "__main__":
    main()
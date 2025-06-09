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
        self._times_list = []

    def add_time(self, elapsed):
        if elapsed < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        self._times_list.append(elapsed)

    @property
    def best_time(self):
        return min(self._times_list) if self._times_list else None

    @property
    def worst_time(self):
        return max(self._times_list) if self._times_list else None

    @property
    def average_time(self):
        return sum(self._times_list) / len(self._times_list) if self._times_list else None

    @property
    def times_list(self):
        return self._times_list.copy()

def main(lang="en"):
    from apps.guis.timer_gui import TimerAppGUI
    app = TimerAppGUI(lang)
    app.run()

if __name__ == "__main__":
    main()
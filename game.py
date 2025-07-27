class Arena:
    def __init__(self, size=10):
        self._size = size
        self._column_size = (size * 2) - 1
        self._row_size = size
        self._arena = [
            ["." if (c % 2 == 0) else " " for c in range(self._column_size)]
            for r in range(self._row_size)
        ]
        self._top_down_border = f"   +{'-' * (self._column_size + 2)}+\n"

    def render_wizard_to_arena(self, position, symbol):
        x, y = position
        self._arena[y][x] = symbol

        # if (x < self._size and x > -1) and (y > -1 and y < self._size):
        #    self._area

    def clean_up_wizard(self, position):
        x, y = position
        self._arena[y][x] = "."

    def __repr__(self) -> str:
        # 4 empty space characters
        render = "    "

        # ASCII values for uppercase letters A - Z range from 65 to 90
        for i in range(65, 65 + self._size):
            render += f"{chr(i)} "

        render += "  \n"
        render += self._top_down_border

        # self.wizzard_position()

        for r in range(self._row_size):
            if r < 10:
                render += " "

            render += f"{r} | "

            for c in range(self._column_size):
                render += self._arena[r][c]

            render += " |\n"

        render += self._top_down_border
        return render


class Wizard:
    def __init__(self, x, y, arena):
        self._symbol = "W"
        self._arena = arena
        self._x = x
        self._y = y

        self.render_wizard_to_arena()

    @property
    def position(self):
        """The position property."""
        return (self._x, self._y)

    @position.setter
    def position(self, position):
        self._arena.clean_up_wizard(self.position)

        self._x, self._y = position

        self.render_wizard_to_arena()


    def render_wizard_to_arena(self):
        self._arena.render_wizard_to_arena(self.position, self._symbol)


def test():
    x = 0
    y = 4
    arena = Arena(size=15)
    wizard = Wizard(x, y, arena)
    print(arena)
    wizard.position = (2, 4)
    print(arena)

    # print(arena)


if __name__ == "__main__":
    test()

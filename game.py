import random
from random import randrange


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
        self._rendered_objects_percentage = 2

    @property
    def arena(self):
        """The arena property."""
        return self._arena

    @arena.setter
    def arena(self, value):
        self._arena = value

    def render_object_to_arena(self, position, symbol):
        x, y = position
        self._arena[y][x] = symbol

    def clean_up_wizard(self, position):
        x, y = position
        self._arena[y][x] = "."

    def __repr__(self) -> str:
        # 4 empty space characters
        render = "     "

        # ASCII values for uppercase letters A - Z range from 65 to 90
        for i in range(65, 65 + self._size):
            render += f"{chr(i)} "

        render += "  \n"
        render += self._top_down_border

        # self.wizzard_position()

        for r in range(self._row_size):
            ln = r + 1
            if ln < 10:
                render += " "

            render += f"{ln} | "

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
        self._crystals = 0
        self._tail = []
        self._tail_symbol = "o"
        self._portal_entry = None
        self._portal_exit = None
        self._portal_symbol = "@"

        self.render_wizard_to_arena()

    @property
    def position(self):
        """The position property."""
        return (self._x, self._y)

    @position.setter
    def position(self, position):
        self._arena.clean_up_wizard(self.position)

        # Update tail positions
        if self._tail:
            # Clean up the last tail segment
            if len(self._tail) >= self._crystals:
                last_segment = self._tail.pop()
                self._arena.clean_up_wizard(last_segment)

            # Add current position to front of tail
            self._tail.insert(0, self.position)

            # Render the tail
            for segment in self._tail:
                self._arena.render_object_to_arena(segment, self._tail_symbol)

        self._x, self._y = position
        self.render_wizard_to_arena()

        # Re-render portals if they exist (in case they were overwritten)
        if self._portal_entry:
            self._arena.render_object_to_arena(self._portal_entry, self._portal_symbol)
        if self._portal_exit:
            self._arena.render_object_to_arena(self._portal_exit, self._portal_symbol)

        # TODO: place in a Arena object helper function
        objects_rendered = len(self._tail) + 2
        size = self._arena._size
        self._arena._rendered_objects_percentage = int((objects_rendered / (size * size)) * 100)

    @property
    def crystals(self):
        return self._crystals

    def collect_crystals(self, crystal):
        self._crystals += 1
        # When collecting a crystal, add current position to tail
        if self.position not in self._tail:
            self._tail.insert(0, self.position)

        crystal.spawn(self)

    def render_wizard_to_arena(self):
        self._arena.render_object_to_arena(self.position, self._symbol)

    def collision(self, game_object):
        return self.position == game_object.position

    def collision_with_tail(self):
        return self.position in self._tail

    def has_active_portal(self):
        return self._portal_entry is not None or self._portal_exit is not None

    def create_portal(self, from_pos, to_pos, crystal):
        self._portal_entry = from_pos
        self._portal_exit = to_pos
        # Render portals
        self._arena.render_object_to_arena(from_pos, self._portal_symbol)
        self._arena.render_object_to_arena(to_pos, self._portal_symbol)
        
        if to_pos == crystal.position:
           self.collect_crystals(crystal)


    def check_portal_clear(self):
        # Check if all tail segments have passed through the portal
        if self._portal_entry and self._portal_exit:
            # Portal is clear when no tail segments are at the entry position
            # and wizard is not at the exit position
            if self._portal_entry not in self._tail and self.position != self._portal_exit:
                # Clean up portals
                self._arena.clean_up_wizard(self._portal_entry)
                self._arena.clean_up_wizard(self._portal_exit)
                self._portal_entry = None
                self._portal_exit = None


class Crystal:
    def __init__(self, x, y, arena):
        self._symbol = "♦"
        self._x = x
        self._y = y
        self._arena = arena

        self.render_crystal_to_arena()

    @property
    def position(self):
        """The position property."""
        return (self._x, self._y)

    @position.setter
    def position(self, position):
        self._x, self._y = position
        self.render_crystal_to_arena()

    def spawn_depreciated(self, wizard: Wizard):
        wx, wy = wizard.position

        spawned = False
        while not spawned:
            # determines where the crystal should be placed on the arena
            x = randrange(0, self._arena._column_size, 2)
            y = randrange(0, self._arena._row_size)

            # Check if position is far enough from wizard AND not on any tail segment
            if abs(x - wx) > 2 and abs(y - wy) > 2:
                # Also check that it's not on any tail segment
                if (x, y) not in wizard._tail:
                    self.position = (x, y)
                    spawned = True

    def spawn(self, wizard: Wizard):
        spawn_points = []

        for y in range(self._arena._row_size):
            for x in range(0, self._arena._column_size, 2):
                if self._arena.arena[y][x] == ".":
                    spawn_points.append((x, y))

        self.position = random.choice(spawn_points)

    def render_crystal_to_arena(self):
        self._arena.render_object_to_arena(self.position, self._symbol)


def test():
    arena = Arena(size=15)
    wizard = Wizard(0, 4, arena)
    crystal = Crystal(6, 7, arena)

    print(arena)


if __name__ == "__main__":
    test()

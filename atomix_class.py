import tkinter

ATOM = "atom"
H = "H"
O = "O"
H1 = "H1"
H2 = "H2"
BG = "BG"
COORDS = "Coords"
DIRECTION = "direction"
DOWN = "Down"
EAST = "east"
LEFT = "Left"
RIGHT = "Right"
TAG = "tag"
UP = "Up"
WEST = "west"
E = "empty"
W = "wall"

LEVEL_01 = [[BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
            [BG, W, W, W, W, W, BG, BG, BG, BG, BG, BG, BG, BG],
            [BG, W, E, E, E, W, BG, BG, BG, BG, BG, BG, BG, BG],
            [BG, W, E, E, E, W, W, W, W, W, W, BG, BG, BG],
            [BG, W, E, E, W, E, E, E, E, E, W, BG, BG, BG],
            [BG, W, E, W, E, E, E, H2, O, E, W, W, BG, BG],
            [BG, W, E, W, E, E, W, E, W, W, E, W, BG, BG],
            [BG, W, E, E, E, E, W, E, W, E, E, W, BG, BG],
            [BG, W, W, W, E, W, E, E, W, E, E, W, BG, BG],
            [BG, W, H1, E, E, E, E, E, E, E, E, W, BG, BG],
            [BG, W, W, W, W, W, W, W, W, W, W, W, BG, BG],
            [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG]]

MOL_01 = [{ATOM: H, DIRECTION: {EAST: 1}, TAG: H1}, {ATOM: H, DIRECTION: {WEST: 1}, TAG: H2},
          {ATOM: O, DIRECTION: {EAST: 1, WEST: 1}, TAG: O}]

MOLECULE_01 = [[H1, O, H2, E, E],
               [E, E, E, E, E],
               [E, E, E, E, E],
               [E, E, E, E, E],
               [E, E, E, E, E]]

DIRECT = {RIGHT: [0, 1], LEFT: [0, -1], UP: [-1, 0], DOWN: [1, 0]}


class Cursor:

    def __init__(self):
        self.i = 1
        self.j = 1
        self.tag = "c"
        self.active = False


class View:
    X = 20
    Y = 20
    ACTIVE_CURSOR_COLOUR = "pink"
    BG_COLOUR = "light grey"
    CIRCLE_DIAMETER = 16
    INACTIVE_CURSOR_COLOUR = "yellow"
    LINE = 5
    SQUARE_SIZE = 30
    WALL_COLOUR = "red"
    WALL_OUTLINE_COLOUR = "blue"

    def __init__(self, canvas):
        self.canvas = canvas

    def convert_to_x(self, j):
        return int(self.X + j * self.SQUARE_SIZE)

    def convert_to_y(self, i):
        return int(self.Y + i * self.SQUARE_SIZE)

    def calculate_center(self, x, y):
        return int(x + self.SQUARE_SIZE / 2), int(y + self.SQUARE_SIZE / 2)

    def draw_wall(self, i, j):
        self.canvas.create_rectangle(self.convert_to_x(j), self.convert_to_y(i), self.convert_to_x(j + 1),
                                     self.convert_to_y(i + 1), fill=self.WALL_COLOUR, outline=self.WALL_OUTLINE_COLOUR)

    def draw_background(self, i, j):
        self.canvas.create_rectangle(self.convert_to_x(j), self.convert_to_y(i), self.X + self.convert_to_x(j + 1),
                                     self.convert_to_y(i + 1), fill=self.BG_COLOUR, outline=self.BG_COLOUR)

    def draw_oval(self, x, y, tag):

        circle_corr = (self.SQUARE_SIZE - self.CIRCLE_DIAMETER) / 2
        self.canvas.create_oval(x + circle_corr, y + circle_corr, x + self.SQUARE_SIZE - circle_corr,
                                y + self.SQUARE_SIZE - circle_corr,
                                tags=tag)

    def line_west(self, number, x, y, tag):
        center = self.calculate_center(x, y)
        circumradius = self.CIRCLE_DIAMETER / 2
        if number == 1:
            self.canvas.create_line(center[0] - circumradius, center[1], center[0] - circumradius - self.LINE,
                                    center[1], tags=tag)

    def line_east(self, number, x, y, tag):
        center = self.calculate_center(x, y)
        circumradius = self.CIRCLE_DIAMETER / 2
        if number == 1:
            self.canvas.create_line(center[0] + circumradius, center[1], center[0] + circumradius + self.LINE,
                                    center[1], tags=tag)

    def line(self, direct, number, x, y, tag):
        if direct == EAST:
            self.line_east(number, x, y, tag)
        elif direct == WEST:
            self.line_west(number, x, y, tag)

    """        elif direct == "south":
            self.line_south(number,  x, y, tag)
        elif direct == "north":
            self.line_north(number,  x, y, tag)
        elif direct == "southwest":
            self.line_southwest(number,  x, y, tag)
        elif direct == "northhwest":
            self.line_northhwest(number,  x, y, tag)
        elif direct == "northeast":
            self.line_northeast(number,  x, y, tag)
        elif direct == "southeast":
            self.line_southeast(number,  x, y, tag)
    """

    def draw_line(self, x, y, directions, tag):
        for key in directions:
            self.line(key, directions[key], x, y, tag)

    def draw_hydrogen(self, atom, j, i):
        x = self.convert_to_x(j)
        y = self.convert_to_y(i)
        self.draw_oval(x, y, atom[TAG])
        self.canvas.create_text(self.calculate_center(x, y), text=atom[ATOM], tags=atom[TAG])
        self.draw_line(x, y, atom[DIRECTION], atom[TAG])

    def draw_oxygen(self, atom, j, i):
        x = self.convert_to_x(j)
        y = self.convert_to_y(i)
        self.draw_oval(x, y, atom[TAG])
        self.canvas.create_text(self.calculate_center(x, y), text=atom[ATOM], tags=atom[TAG])
        self.draw_line(x, y, atom[DIRECTION], atom[TAG])

    def draw_cursor(self, i, j, tag, active):

        x = self.convert_to_x(j)
        y = self.convert_to_y(i)
        if active is False:
            self.canvas.create_line(x, y, x + self.SQUARE_SIZE, y, fill=self.INACTIVE_CURSOR_COLOUR, width=3, tags=tag)
            self.canvas.create_line(x, y, x, y + self.SQUARE_SIZE, fill=self.INACTIVE_CURSOR_COLOUR, width=3, tags=tag)
            self.canvas.create_line(x + self.SQUARE_SIZE, y, x + self.SQUARE_SIZE, y + self.SQUARE_SIZE,
                                    fill=self.INACTIVE_CURSOR_COLOUR, width=3, tags=tag)
            self.canvas.create_line(x, y + self.SQUARE_SIZE, x + self.SQUARE_SIZE, y + self.SQUARE_SIZE,
                                    fill=self.INACTIVE_CURSOR_COLOUR, width=3, tags=tag)
        else:
            self.canvas.create_line(x, y, x + self.SQUARE_SIZE, y, fill=self.ACTIVE_CURSOR_COLOUR, width=3, tags=tag)
            self.canvas.create_line(x, y, x, y + self.SQUARE_SIZE, fill=self.ACTIVE_CURSOR_COLOUR, width=3, tags=tag)
            self.canvas.create_line(x + self.SQUARE_SIZE, y, x + self.SQUARE_SIZE, y + self.SQUARE_SIZE,
                                    fill=self.ACTIVE_CURSOR_COLOUR, width=3, tags=tag)
            self.canvas.create_line(x, y + self.SQUARE_SIZE, x + self.SQUARE_SIZE, y + self.SQUARE_SIZE,
                                    fill=self.ACTIVE_CURSOR_COLOUR, width=3, tags=tag)

    def draw_success(self):
        self.canvas.create_text(self.X + self.SQUARE_SIZE * 5, self.Y + self.SQUARE_SIZE * 5, text="WIN",
                                font="Times 30 bold")

    def delete_element(self, tag):
        self.canvas.delete(tag)


class Model:

    def __init__(self, level, mol, direct, molecule, view):
        self.level = level
        self.mol = mol
        self.cursor = Cursor()
        self.view = view
        self.direct = direct
        self.molecule = molecule

    def draw_background_model(self):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == BG:
                    self.view.draw_background(i, j)

    def draw_wall_model(self):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == W:
                    self.view.draw_wall(i, j)

    def draw_atom(self, i, j):
        for k in range(len(self.mol)):
            if self.level[i][j] == self.mol[k][TAG]:
                if self.mol[k][ATOM] == H:
                    self.view.draw_hydrogen(self.mol[k], j, i)
                elif self.mol[k][ATOM] == O:
                    self.view.draw_oxygen(self.mol[k], j, i)

    def draw_atoms(self):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] != W and self.level[i][j] != E:
                    self.draw_atom(i, j)

    def draw_cursor_model(self):
        self.view.draw_cursor(self.cursor.i, self.cursor.j, self.cursor.tag, self.cursor.active)

    def is_cursor_active(self):
        return self.cursor.active

    def is_field_occupied(self, i, j):
        if self.level[i][j] != E and self.level[i][j] != W:
            return True

    def change_cursor_activation(self):
        if self.cursor.active:
            self.cursor.active = False
            self.view.draw_cursor(self.cursor.i, self.cursor.j, self.cursor.tag, False)
        else:
            self.cursor.active = True
            self.view.draw_cursor(self.cursor.i, self.cursor.j, self.cursor.tag, True)

    def will_be_cursor_on_the_map(self, direction):
        return self.level[self.cursor.i + self.direct[direction][0]][self.cursor.j + self.direct[direction][1]] != BG

    def change_cursor_position(self, direction):
        self.cursor.i = self.cursor.i + self.direct[direction][0]
        self.cursor.j = self.cursor.j + self.direct[direction][1]

    def delete_element_model(self, tag):
        self.view.delete_element(tag)

    def move_cursor(self, direction):
        self.change_cursor_position(direction)
        self.delete_element_model(self.cursor.tag)
        self.draw_cursor_model()

    def put_cursor_into_new_position(self, direction):
        i = self.cursor.i + self.direct[direction][0]
        j = self.cursor.j + self.direct[direction][1]
        if self.level[i][j] != E:
            return
        self.change_cursor_position(direction)
        self.put_cursor_into_new_position(direction)

    def calculate_coords_in_map(self, tag):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == tag:
                    return i, j

    def calculate_coords(self, tag):
        for i in range(len(self.molecule)):
            for j in range(len(self.molecule[i])):
                if self.molecule[i][j] == tag:
                    return i, j

    def calculate_number(self):
        coords_in_map = self.calculate_coords_in_map(self.mol[0][TAG])
        coords = self.calculate_coords(self.mol[0][TAG])
        number = [coords_in_map[0] - coords[0], coords_in_map[1] - coords[1]]
        return number

    def check_molecule(self):
        number = self.calculate_number()
        for atom in self.mol:
            coords_in_map = self.calculate_coords_in_map(atom[TAG])
            coords = self.calculate_coords(atom[TAG])
            diff = [coords_in_map[0] - coords[0], coords_in_map[1] - coords[1]]
            if number != diff:
                return False
        return True

    def move_cursor_and_atom(self, direction):
        temp_i = self.cursor.i
        temp_j = self.cursor.j
        self.put_cursor_into_new_position(direction)
        if temp_i == self.cursor.i and temp_j == self.cursor.j:
            return
        self.delete_element_model(self.cursor.tag)
        self.draw_cursor_model()
        self.level[self.cursor.i][self.cursor.j] = self.level[temp_i][temp_j]
        self.delete_element_model(self.level[temp_i][temp_j])
        self.level[temp_i][temp_j] = E
        self.draw_atom(self.cursor.i, self.cursor.j)
        if self.check_molecule():
            self.view.draw_success()

    def move(self, direction):
        if not self.is_cursor_active() and self.will_be_cursor_on_the_map(direction):
            self.move_cursor(direction)
        elif self.is_cursor_active():
            self.move_cursor_and_atom(direction)

    def enter(self):
        if not self.is_cursor_active() and self.is_field_occupied(self.cursor.i, self.cursor.j):
            self.change_cursor_activation()
        elif self.is_cursor_active():
            self.change_cursor_activation()


class Control:
    EVENT_RIGHT = "Right"
    EVENT_LEFT = "Left"
    EVENT_UP = "Up"
    EVENT_DOWN = "Down"
    RETURN = "Return"

    def __init__(self, model, view, canvas):
        self.model = model
        self.view = view
        self.canvas = canvas
        self.canvas.bind_all('<Return>', self.enter)
        self.canvas.bind_all('<Key>', self.move)

    def enter(self, event):
        if event.keysym == self.RETURN:
            self.model.enter()

    def move(self, event):

        if event.keysym == self.EVENT_RIGHT:
            self.model.move(self.EVENT_RIGHT)
        if event.keysym == self.EVENT_LEFT:
            self.model.move(self.EVENT_LEFT)
        if event.keysym == self.EVENT_UP:
            self.model.move(self.EVENT_UP)
        if event.keysym == self.EVENT_DOWN:
            self.model.move(self.EVENT_DOWN)


class Application:
    CANVAS_COLOUR = "light grey"
    TITLE = "Atomix"

    def run(self):
        window = tkinter.Tk()
        window.title(self.TITLE)
        canvas = tkinter.Canvas(window, bg=self.CANVAS_COLOUR, height=600, width=600)
        canvas.pack()
        view = View(canvas)
        model = Model(LEVEL_01, MOL_01, DIRECT, MOLECULE_01, view)
        control = Control(model, view, canvas)
        model.draw_background_model()
        model.draw_wall_model()
        model.draw_atoms()
        model.draw_cursor_model()
        window.mainloop()


if __name__ == "__main__":
    app = Application()
    app.run()

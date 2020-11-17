import tkinter
import copy

SQUARE_SIZE = 30
X1 = 20
Y1 = 20
CIRCLE_DIAMETER = 16
LINE = 5
MOLECULE = [["H", [80, 110], {"east": 1}, "H1"], ["H", [200, 50], {"west": 1}, "H2"], ["O", [170, 230], {"east": 1, "west": 1}, "O"]]



field_01 = [[1,1,1,1,1,1,1,   1],
            [1,0,0,0,1,1,"H2",1],
            [1,0,1,1,1,0,0,   1],
            [1,0,"H1",0,0,0,0,1],
            [1,0,0,0,0,0,0,   1],
            [1,0,0,1,0,0,0,   1],
            [1,0,0,1,0,0,0,   1],
            [1,0,0,1,0,"O",0, 1],
            [1,0,0,0,0,0,0,   1],
            [1,1,1,1,1,1,1,   1]]

MAX_RIGHT_SIDE = SQUARE_SIZE * (len(field_01[0]) - 1)

MAX_DOWN_SIDE = SQUARE_SIZE * (len(field_01) - 1)

def convert_to_j(X):
    
   return (X - X1) / SQUARE_SIZE
    

def convert_to_i(Y):   
    
    return (Y - Y1) / SQUARE_SIZE 



def draw_field(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1:
                canvas.create_rectangle(X1 + SQUARE_SIZE * j, Y1 + SQUARE_SIZE * i, X1 + SQUARE_SIZE + SQUARE_SIZE * j, Y1 + SQUARE_SIZE + SQUARE_SIZE * i, fill = "red", outline = "blue")


def calculate_center(start_pos):
    return start_pos[0] + SQUARE_SIZE / 2 , start_pos[1] + SQUARE_SIZE / 2

def draw_oval(start_pos, tag):
    
    circle_corr = (SQUARE_SIZE - CIRCLE_DIAMETER) / 2
    canvas.create_oval(start_pos[0] + circle_corr , start_pos[1] + circle_corr, start_pos[0] + SQUARE_SIZE - circle_corr, start_pos[1] + SQUARE_SIZE - circle_corr, outline = "black", tags = tag)
    
   
def line_west(number, start_pos, tag):
    center = calculate_center(start_pos)  
    circumradius = CIRCLE_DIAMETER / 2
    if number == 1:
        canvas.create_line(center[0] - circumradius, center[1], center[0] - circumradius - LINE, center[1], tags = tag)
    
def line_east(number, start_pos, tag):
    center = calculate_center(start_pos)  
    circumradius = CIRCLE_DIAMETER / 2
    if number == 1:
        canvas.create_line(center[0] + circumradius, center[1], center[0] + circumradius + LINE, center[1], tags = tag)

    
"""def line_north():
def line_south():
def line_northeast():
def line_southeast():
def line_northwest():
def line_southwest():"""


def line(direct, number, start_pos, tag):
    if direct == "east":
        line_east(number, start_pos, tag)
    elif direct == "west":
        line_west(number, start_pos, tag)
    elif direct == "south":
        line_south(number, start_pos)
    elif direct == "north":
        line_north(number, start_pos)
    elif direct == "southwest":
        line_southwest(number, start_pos)
    elif direct == "northhwest":
        line_northhwest(number, start_pos)
    elif direct == "northeast":
        line_northeast(number, start_pos)
    elif direct == "southeast":
        line_southeast(number, start_pos)

        
def draw_line(start_pos, directions, tag):    
    for direct, number in directions.items():
        line(direct, number, start_pos, tag) 
    

def draw_H(atom):
    draw_oval(atom[1], atom[3])
    print(canvas.coords(canvas.create_text(calculate_center(atom[1]), text = atom[0], tags = atom[3])))
    draw_line(atom[1], atom[2], atom[3])
                

def draw_O(atom):    
    draw_oval(atom[1], atom[3])
    canvas.create_text(calculate_center(atom[1]), text = atom[0], tags = atom[3])
    draw_line(atom[1], atom[2], atom[3])

def draw_atom(atom):
    if atom[0] == "H":       
        draw_H(atom)
    elif atom[0] == "O":
        draw_O(atom)
    
def draw_atoms_in_molecule(MOLECULE):  
    for i in range(len(MOLECULE)):
        draw_atom(MOLECULE[i])

def cursor_coord(cursor):
    return canvas.coords(cursor)
    
def check_block(field):
    atom_coords = canvas.coords("H1")
    print(atom_coords)
    
    #print(convert_to_i(atom_coords)[1])
    if field[convert_to_i(atom_coords)[1]][convert_to_j((atom_coords)[0] + 30)] == 1 or atom_coords == canvas.coords("H1") or atom_coords == canvas.coords("H2") or atom_coords == canvas.coords("O"):
        return False 


class MyObj:
    def __init__(self, field):
        self.field = field

        
    def move_atom_and_cursor(self, event):
        if event.keysym == "Right" and cursor_coord(cursor)[0] < MAX_RIGHT_SIDE and canvas.itemcget(cursor, "outline") == "yellow":
            canvas.move(cursor, 30, 0)
        elif event.keysym == "Right" and canvas.itemcget(cursor, "outline") == "pink" and check_block(self.field):
            canvas.move("H1", 30, 0)
            canvas.move(cursor, 30, 0)
        elif event.keysym == "Left" and cursor_coord(cursor)[0] > X1 and canvas.itemcget(cursor, "outline") == "yellow":
            canvas.move(cursor, -30, 0)
        elif event.keysym == "Left" and canvas.itemcget(cursor, "outline") == "pink":
            canvas.move("H1", -30, 0)
            canvas.move(cursor, -30, 0)
        elif event.keysym == "Up" and cursor_coord(cursor)[1] > Y1 and canvas.itemcget(cursor, "outline") == "yellow":
            canvas.move(cursor, 0, -30)
        elif event.keysym == "Up" and canvas.itemcget(cursor, "outline") == "pink":
            canvas.move("H1", 0, -30)
            canvas.move(cursor, 0, -30)
        elif event.keysym == "Down" and cursor_coord(cursor)[1] < MAX_DOWN_SIDE and canvas.itemcget(cursor, "outline") == "yellow":
            canvas.move(cursor, 0, 30)
        elif event.keysym == "Down" and canvas.itemcget(cursor, "outline") == "pink":
            canvas.move("H1", 0, 30)
            canvas.move(cursor, 0, 30)
    


def use_Enter(event):
    if event.keysym == "Return" and canvas.itemcget(cursor, "outline") == "yellow":
        
        for atom in moved_molecule:
            if atom[1][0] == cursor_coord(cursor)[0] and atom[1][1] == cursor_coord(cursor)[1]:
                canvas.itemconfig(cursor, outline = "pink", width = 3)
                
    elif event.keysym == "Return" and canvas.itemcget(cursor, "outline") == "pink":
        canvas.itemconfig(cursor, outline = "yellow", width = 1)



window = tkinter.Tk()
window.title("Atomix")
canvas = tkinter.Canvas(window, bg = "light grey", height = 600, width = 600)
canvas.pack()
draw_field(field_01)
draw_atoms_in_molecule(MOLECULE)
new_field = copy.deepcopy(field_01)
moved_molecule = copy.deepcopy(MOLECULE)
cursor = canvas.create_rectangle(X1, Y1, X1 + SQUARE_SIZE, Y1 + SQUARE_SIZE, outline = "yellow")

obj = MyObj(field_01)



canvas.bind_all('<Key>', obj.move_atom_and_cursor)
canvas.bind_all('<Return>', use_Enter)









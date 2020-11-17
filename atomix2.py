import tkinter
import copy

SQUARE_SIZE = 30
X = 20
Y = 20
CIRCLE_DIAMETER = 16
LINE = 5
MOL = [["H", {"east": 1}, "H1"], ["H", {"west": 1}, "H2"], ["O", {"east": 1, "west": 1}, "O"]]

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

def convert_to_j(x):   
   return int((x - X) / SQUARE_SIZE)

def convert_to_i(y):      
    return int((y - Y) / SQUARE_SIZE) 

def convert_to_x(j):
    return int(X + j * SQUARE_SIZE)

def convert_to_y(i):
    return int(Y + i * SQUARE_SIZE)
    
def calculate_center(x, y):
    return int(x + SQUARE_SIZE / 2) , int(y + SQUARE_SIZE / 2)

def draw_line(x, y, directions, tag):    
    for direct, number in directions.items():
        line(direct, number, x, y, tag) 

def line_west(number, x, y, tag):
    center = calculate_center(x, y)  
    circumradius = CIRCLE_DIAMETER / 2
    if number == 1:
        canvas.create_line(center[0] - circumradius, center[1], center[0] - circumradius - LINE, center[1], tags = tag)
    
def line_east(number, x, y, tag):
    center = calculate_center(x, y)  
    circumradius = CIRCLE_DIAMETER / 2
    if number == 1:
        canvas.create_line(center[0] + circumradius, center[1], center[0] + circumradius + LINE, center[1], tags = tag)

def line(direct, number, x, y, tag):
    if direct == "east":
        line_east(number,  x, y, tag)
    elif direct == "west":
        line_west(number,  x, y, tag)
    elif direct == "south":
        line_south(number,  x, y, tag)
    elif direct == "north":
        line_north(number,  x, y, tag)
    elif direct == "southwest":
        line_southwest(number,  x, y, tag)
    elif direct == "northhwest":
        line_northhwest(number,  x, y, tag)
    elif direct == "northeast":
        line_northeast(number,  x, y, tag)
    elif direct == "southeast":
        line_southeast(number,  x, y, tag)


def draw_oval(x, y, tag):   
    circle_corr = (SQUARE_SIZE - CIRCLE_DIAMETER) / 2
    canvas.create_oval(x + circle_corr , y + circle_corr, x + SQUARE_SIZE - circle_corr, y + SQUARE_SIZE - circle_corr, outline = "black", tags = tag)

def draw_H(atom, x, y):
    draw_oval(x, y, atom[2])
    canvas.create_text(calculate_center(x, y), text = atom[0], tags = atom[2])
    draw_line(x, y, atom[1], atom[2])
    
def draw_O(atom, x, y):    
    draw_oval(x, y, atom[2])
    canvas.create_text(calculate_center(x, y), text = atom[0], tags = atom[2])
    draw_line(x, y, atom[1], atom[2])
    
def draw_atom(atom, x, y):
    if atom[0]== "H":       
        draw_H(atom, x, y)
    elif atom[0] == "O":
        draw_O(atom, x, y)
        
def draw_field(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1:
                canvas.create_rectangle(X + SQUARE_SIZE * j, Y + SQUARE_SIZE * i, X + SQUARE_SIZE + SQUARE_SIZE * j, Y + SQUARE_SIZE + SQUARE_SIZE * i, fill = "red", outline = "blue")
            elif field[i][j] == 0:
                pass
            else:
                for k in range(len(MOL)):
                    if field[i][j] == MOL[k][2]:
                        draw_atom(MOL[k], convert_to_x(j), convert_to_y(i))




def use_Enter(event):
    if event.keysym == "Return" and canvas.itemcget(cursor, "outline") == "yellow":
        i = convert_to_i(canvas.coords(cursor)[1])
        j = convert_to_j(canvas.coords(cursor)[0])
        if copied_field[i][j] != 1 and copied_field[i][j] != 0:
            canvas.itemconfig(cursor, outline = "pink", width = 3)                 
    elif event.keysym == "Return" and canvas.itemcget(cursor, "outline") == "pink":
        canvas.itemconfig(cursor, outline = "yellow", width = 1)
        

def calculate_new_coords(x, y, direct, field):
    print(x, y)
    j = convert_to_j(x)
    i = convert_to_i(y)
    print(i, j)
    if direct == "Right":
        for k in range(j + 1, len(field[i])):
            
            if copied_field[i][k] != 0:
                #print(convert_to_x(k - 1), convert_to_y(i))
                return convert_to_x(k - 1), convert_to_y(i)
            
def insert_into_matrix(name_in_matrix, x, y, field):
        field[convert_to_i(y)][convert_to_j(x)] = name_in_matrix


def calculate_move_distance(x, y, direct, field):
    new_x = calculate_new_coords(x, y, direct, field)[0]
    new_y = calculate_new_coords(x, y, direct, field)[1]
    
    
    if new_x == x :
        return new_y - y
    else:
        return new_x - x
        
    
def move_atom(x, y, direct, field):
    i = convert_to_i(y)
    j = convert_to_j(x)
    for k in range(len(MOL)):
        if field[i][j] == MOL[k][2]:
            canvas.delete(MOL[k][2])
            #print(calculate_new_coords(x, y, direct, field)[0], calculate_new_coords(x, y, direct, field)[1])
            draw_atom(MOL[k], calculate_new_coords(x, y, direct, field)[0], calculate_new_coords(x, y, direct, field)[1])
            insert_into_matrix(MOL[k][2], calculate_new_coords(x, y, direct, field)[0], calculate_new_coords(x, y, direct, field)[1], field)
            field[i][j] = 0
    
    
class MyObj:
    def __init__(self, field):
        self.field = field

        
    def move_atom_and_cursor(self, event):
        cursor_x = canvas.coords(cursor)[0]
        cursor_y = canvas.coords(cursor)[1]

        
        if event.keysym == "Right" and cursor_x < MAX_RIGHT_SIDE and canvas.itemcget(cursor, "outline") == "yellow":
            canvas.move(cursor, 30, 0)
        elif event.keysym == "Right" and canvas.itemcget(cursor, "outline") == "pink":
            move_atom(cursor_x, cursor_y, event.keysym, self.field)
            canvas.move(cursor, calculate_move_distance(cursor_x, cursor_y, event.keysym, self.field), 0)   
        elif event.keysym == "Left" and cursor_x > X and canvas.itemcget(cursor, "outline") == "yellow":
            canvas.move(cursor, -30, 0)
        elif event.keysym == "Left" and canvas.itemcget(cursor, "outline") == "pink":
            move_atom(cursor_x, cursor_y, event.keysym, self.field)
            canvas.move(cursor, calculate_move_distance(cursor_x, cursor_y, event.keysym, self.field), 0)  
        elif event.keysym == "Up" and cursor_y > Y and canvas.itemcget(cursor, "outline") == "yellow":
            canvas.move(cursor, 0, -30)
        elif event.keysym == "Up" and canvas.itemcget(cursor, "outline") == "pink":
            move_atom(cursor_x, cursor_y, event.keysym, self.field)
            canvas.move(cursor, calculate_move_distance(cursor_x, cursor_y, event.keysym, self.field), 0)  
        elif event.keysym == "Down" and cursor_y < MAX_DOWN_SIDE and canvas.itemcget(cursor, "outline") == "yellow":
            canvas.move(cursor, 0, 30)
        elif event.keysym == "Down" and canvas.itemcget(cursor, "outline") == "pink":
            move_atom(cursor_x, cursor_y, event.keysym, self.field)
            canvas.move(cursor, calculate_move_distance(cursor_x, cursor_y, event.keysym, self.field), 0)  
        
window = tkinter.Tk()
window.title("Atomix")
canvas = tkinter.Canvas(window, bg = "light grey", height = 600, width = 600)
canvas.pack()
draw_field(field_01)
copied_field = copy.deepcopy(field_01)
copied_molecule = copy.deepcopy(MOL)
cursor = canvas.create_rectangle(X, Y, X + SQUARE_SIZE, Y + SQUARE_SIZE, outline = "yellow")
obj = MyObj(copied_field)
canvas.bind_all('<Key>', obj.move_atom_and_cursor)
canvas.bind_all('<Return>', use_Enter)
print(copied_field)

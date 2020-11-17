"""def convert_to_X1(j):
    X1 = X1 + j * SQUARE_SIZE
    

def convert_to_Y1(i):   
    Y1 = Y1 + i * SQUARE_SIZE

def move_cursor_left(cursor):
    
        canvas.create_rectangle(cursor[0], cursor[1], cursor[0] + SQUARE_SIZE, cursor[1] + SQUARE_SIZE, outline = "red")
        canvas.create_rectangle(cursor[0] - SQUARE_SIZE, cursor[1]  , cursor[0], cursor[1] + SQUARE_SIZE, outline = "yellow")
        cursor = [cursor[0] - SQUARE_SIZE, cursor[1]]
        

def move_cursor_right(cursor):
        canvas.create_rectangle(cursor[0], cursor[1], cursor[0] + SQUARE_SIZE, cursor[1] + SQUARE_SIZE, outline = "red")
        canvas.create_rectangle(cursor[0] + SQUARE_SIZE, cursor[1]  , cursor[0] + 2 * SQUARE_SIZE, cursor[1] + SQUARE_SIZE, outline = "yellow")
        cursor = [cursor[0] + SQUARE_SIZE, cursor[1]]"""




"""cursor = [X1, Y1]
canvas.create_rectangle(X1, Y1, X1 + SQUARE_SIZE, Y1 + SQUARE_SIZE, outline = "yellow")

class MyObj:
    def __init__(self, cursor):
        self.cursor = cursor

    def move_cursor_right(self, event):
        
        canvas.create_rectangle(self.cursor[0], self.cursor[1], self.cursor[0] + SQUARE_SIZE, self.cursor[1] + SQUARE_SIZE, outline = "blue")
        canvas.create_rectangle(self.cursor[0] + SQUARE_SIZE, self.cursor[1]  , self.cursor[0] + 2 * SQUARE_SIZE, self.cursor[1] + SQUARE_SIZE, outline = "yellow")
        self.cursor = [self.cursor[0] + SQUARE_SIZE, self.cursor[1]]

    def move_cursor_left(self, event):   
        canvas.create_rectangle(self.cursor[0], self.cursor[1], self.cursor[0] + SQUARE_SIZE, self.cursor[1] + SQUARE_SIZE, outline = "blue")
        canvas.create_rectangle(self.cursor[0] - SQUARE_SIZE, self.cursor[1]  , self.cursor[0], self.cursor[1] + SQUARE_SIZE, outline = "yellow")
        self.cursor = [self.cursor[0] - SQUARE_SIZE, self.cursor[1]]

    def move_cursor_down(self, event):
        canvas.create_rectangle(self.cursor[0], self.cursor[1], self.cursor[0] + SQUARE_SIZE, self.cursor[1] + SQUARE_SIZE, outline = "blue")
        canvas.create_rectangle(self.cursor[0], self.cursor[1] + SQUARE_SIZE, self.cursor[0] + SQUARE_SIZE, self.cursor[1] + 2 * SQUARE_SIZE, outline = "yellow")
        self.cursor = [self.cursor[0], self.cursor[1] + SQUARE_SIZE]


obj = MyObj(cursor)

canvas.bind_all("<Left>", obj.move_cursor_left)
canvas.bind_all("<Right>", obj.move_cursor_right)
canvas.bind_all("<Down>", obj.move_cursor_down)"""




def move_cursor(event, cursor):
    if event.keysym == "Right" and cursor_coord_X1(cursor) < MAX_WEIGHT :
        canvas.move(cursor, 30, 0)
    elif event.keysym == "Left":
        canvas.move(cursor, -30, 0)
    elif event.keysym == "Up":
        canvas.move(cursor, 0, -30)
    if event.keysym == "Down":
        canvas.move(cursor, 0, 30)




def move_cursor(event):
    if event.keysym == "Right" and cursor_coord(cursor)[0] < MAX_RIGHT_SIDE:
        canvas.move(cursor, 30, 0)
    elif event.keysym == "Left" and cursor_coord(cursor)[0] > X1:
        canvas.move(cursor, -30, 0)
    elif event.keysym == "Up" and cursor_coord(cursor)[1] > Y1:
        canvas.move(cursor, 0, -30)
    elif event.keysym == "Down" and cursor_coord(cursor)[1] < MAX_DOWN_SIDE:
        canvas.move(cursor, 0, 30)


def create_blocks_coords(field):
    block = list()
    blocks_row = list()
    blocks = list()
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1:
                block.append(X1 + j * SQUARE_SIZE)
                block.append(Y1 + i * SQUARE_SIZE)
                blocks_row.append(block)
        blocks.append(blocks_row)
    return  blocks

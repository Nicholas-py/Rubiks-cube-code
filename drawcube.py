import tkinter as tk
import threading
from collections import deque
# # Map colors (edit as needed)
color_map = {
     'W': 'white',
     'Y': 'yellow',
     'R': 'red',
     'O': 'orange',
     'G': 'green',
     'B': 'blue',
 }


# tile = 30
# origin_x = 300
# origin_y = 150

# # Skewing parameters
# dx = tile  # horizontal size of one tile
# dy = tile // 2  # vertical skew for top face
# flap_dy = tile // 3

# def draw_tile(points, color, canvas):
#     canvas.create_polygon(points, fill=color, outline="black")

# def draw_face(face, face_type, canvas):
#     """Draws one of the 3 visible faces in isometric projection."""
#     for i in range(3):
#         for j in range(3):
#             color = color_map[face[i][j]]

#             if face_type == 'U':
#                 # Top face (tilted backward)
#                 x = origin_x + ((2-j) - (2-i)) * dx // 2
#                 y = origin_y + ((2-j) + (2-i)) * dy // 2
#                 points = [
#                     (x, y),
#                     (x + dx // 2, y + dy // 2),
#                     (x, y + dy),
#                     (x - dx // 2, y + dy // 2)
#                 ]

#             elif face_type == 'F':
#                 # Front face (vertical)
#                 x = origin_x + (j - 1) * dx // 2 - dx
#                 y = origin_y + dy * 1.5 + i * dy
#                 points = [
#                     (x, y + j*dy//2),
#                     (x + dx // 2, y + dy // 2 + j*dy//2),
#                     (x + dx // 2, y + dy // 2 + dy+ j*dy//2),
#                     (x, y + dy+ j*dy//2)
#                 ]

#             elif face_type == 'R':
#                 # Right face (skewed side)
#                 x = origin_x  + j * dx // 2
#                 y = origin_y + (i - j/2) * dy  + dy * 3
#                 points = [
#                     (x, y),
#                     (x + dx // 2, y - dy // 2),
#                     (x + dx // 2, y - dy // 2 + dy),
#                     (x, y + dy)
#                 ]

#             draw_tile(points, color, canvas)

# # Draw main cube faces

# # Draw flap faces
# view = [0, 1, 2, 3, 4, 5]
# def draw_cube(cube, canvas):
#     # Draw the 3 visible faces
#     F, L, B, R, D, U = [cube[i] for i in view]

#     draw_face(U, 'U', canvas)  # Up
#     draw_face(F, 'F', canvas)  # Front
#     draw_face(R, 'R', canvas)  # Right

# def rotate_view_right(canvas):
#     global view
#     F, L, B, R, D, U = view
#     view = [L, B, R, F, D, U]
#     draw_cube(lastcube, canvas)

# def rotate_view_left(canvas):
#     # F → L, L → B, B → R, R → F
#     global view
#     F, L, B, R, D, U = view
#     view = [R, F, L, B, D, U]
#     draw_cube(lastcube, canvas)

# def rotate_view_up(canvas):
#     global view
#     F, L, B, R, D, U = view
#     view = [D, L, U, R, B, F]
#     draw_cube(lastcube, canvas)

# def rotate_view_down(canvas):
#     global view
#     F, L, B, R, D, U = view
#     view = [U, L, D, R, F, B]
#     draw_cube(lastcube, canvas)


# Draw one face at a given (x, y)
def draw_face(canvas, cube, face, x, y, size=30):
    
    for i in range(len(cube[0])):
        for j in range(len(cube[0])):
            # if face in [5]:
            #     k = 2-j
            #     l = 2-i
            # elif face in [4]:
            #     k = j
            #     l = i
            # elif face in [2]:
            #     k = 2-j
            #     l = 2-i
            # else:
            k = j
            l = i

            color = color_map.get(cube[face][k][l], 'gray')
            canvas.create_rectangle(
                x + i*size, y + j*size,
                x + (i+1)*size, y + (j+1)*size,
                fill=color, outline='black'
            )

def draw_cube(cube, canvas):
    size = 30
    offset = 10  # margin
    gap = 3

    # Layout coordinates
    coords = {
        5: (size*len(cube[0]) + offset, offset-gap),             # Up
        1: (offset-gap, size*len(cube[0]) + offset),             # Left
        0: (size*len(cube[0]) + offset, size*len(cube[0]) + offset),    # Front
        3: (size*2*len(cube[0]) + offset+gap, size*len(cube[0]) + offset),    # Right
        4: (size*len(cube[0]) + offset, size*2*len(cube[0]) + offset+gap),    # Down
        2: (size*len(cube[0]) + offset, size*3*len(cube[0]) + offset+2*gap),  # Back "popup"
    }

    for face_num, (x, y) in coords.items():
        draw_face(canvas, cube,face_num, x, y, size)

def draw(cube):
     updatequeue.append(cube)
lastcube = None
updatequeue = deque()
def updateloop(root,canvas, timeout = 50):
    global lastcube
    if len(updatequeue) > 0:
        lastcube = updatequeue.popleft()
        draw_cube(lastcube, canvas)
    root.after(timeout,updateloop,root,canvas,timeout)



def initialize():
    global lastcube
    n=2
    startcube = [[list(color * n) for _ in range(n)] for color in ['W', 'O', 'Y', 'R', 'G', 'B']]
    root = tk.Tk()
    root.title("Rubik's Cube Viewer")

    canvas = tk.Canvas(root, width=500, height=500, bg='lightgray')
    lastcube=startcube
    canvas.pack()
    updateloop(root,canvas)
    draw_cube(startcube, canvas)
    root.mainloop()





# Run GUI in a separate thread
threading.Thread(target=initialize, daemon=True).start()
from time import sleep

from tkinter import Tk, Canvas
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from scipy import ndimage as ndi
from pathlib import Path


# Press f to fill white color within closed shape
# Press s to save img and proceed to the next one :)
# To exit prematurely, just close the terminal

IMG_FOLDER_PATH = "data/prelabled" # Path for uncompleted gt (input)  
OUTPUT_FOLDER_PATH = "data/output" # Path for completed gt (output)
BRUSH = 4 # Brush size

def redraw():
    global tk_img
    tk_img = ImageTk.PhotoImage(img)
    canvas.itemconfig(canvas_img, image=tk_img)

def paint(e):
    x, y = e.x, e.y
    canvas.create_oval(x-BRUSH, y-BRUSH, x+BRUSH, y+BRUSH,
                       fill="white", outline="")
    draw.ellipse((x-BRUSH, y-BRUSH, x+BRUSH, y+BRUSH), fill=255)

def fill_shape(event=None):
    arr = np.array(img) > 0
    filled = ndi.binary_fill_holes(arr)
    img.paste(Image.fromarray((filled * 255).astype("uint8")))
    redraw()

def save_and_exit(img):
    img.save(output_path)
    root.destroy()

folder = Path(IMG_FOLDER_PATH)
for f in folder.iterdir():
    if f.is_file():
        img_path = f"{IMG_FOLDER_PATH}/{f.name}"
        output_path = f"{OUTPUT_FOLDER_PATH}/{f.name}"
        print(f.name)
        
        img = Image.open(img_path).convert("L")
        img = img.point(lambda p: 255 if p > 0 else 0)
        draw = ImageDraw.Draw(img)

        root = Tk()
        root.title(img_path)
        canvas = Canvas(root, width=img.width, height=img.height)
        canvas.pack()

        tk_img = ImageTk.PhotoImage(img)
        canvas_img = canvas.create_image(0, 0, anchor="nw", image=tk_img)
        
        canvas.bind("<B1-Motion>", paint)

        root.bind("f", fill_shape)
        root.bind("s", lambda e: save_and_exit(img))

        print("Press f to fill. Press s to save.")
        root.mainloop()
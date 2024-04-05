import tkinter as tk
from PIL import Image, ImageTk
import time
import threading
import time


class OverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('100x100')
        self.root.wm_attributes("-transparentcolor", "black")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.offset_x, self.offset_y = None, None
        self.root.bind("<Button-1>", self.on_mouse_click)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_rel)

        
        self.image = Image.open("pandanorm.jpg")
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.background_label = tk.Label(root, image=self.photo_image, bg="black")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
    def on_key_press(self, event, image):
        if event.char == 'p': 
            self.change_background(image)

    def change_background(self, new_image):
        image = Image.open(new_image)
        photo_image = ImageTk.PhotoImage(image)
        self.background_label.config(image=photo_image)
        self.background_label.image = photo_image

    def on_mouse_click(self, event):
        self.offset_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        self.offset_y = self.root.winfo_pointery() - self.root.winfo_rooty()

    def on_mouse_drag(self, event):
        if None not in (self.offset_x, self.offset_y):
            new_window_x = self.root.winfo_pointerx() - self.offset_x
            new_window_y = self.root.winfo_pointery() - self.offset_y
            self.root.geometry("+%d+%d" % (new_window_x, new_window_y))

    def on_mouse_rel(self, event):
        self.offset_x, self.offset_y = None, None
        
    def start_timer(self, duration, image):
    
        timer_thread = threading.Thread(target=self.timer, args=(duration, image))
        timer_thread.start()

    def timer(self, duration, image):
        time.sleep(duration)
        self.change_background(image)

        
        
    
        
        
root = tk.Tk()
app = OverlayApp(root)

root.bind("<Key>", lambda event: app.on_key_press(event, "panda.jpg"))
app.start_timer(2, "pandaspook.jpg")

root.mainloop()

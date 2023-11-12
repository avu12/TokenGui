import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.colorchooser import askcolor
from tkinter import *

class Token:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.token = canvas.create_oval(x, y, x + 30, y + 30, fill="blue", tags="token")
        self.label = canvas.create_text(x + 15, y + 15, text="", tags="token_label", fill="white")
        self.canvas.tag_bind(self.token, "<ButtonPress-1>", self.on_token_click)
        self.canvas.tag_bind(self.token, "<B1-Motion>", self.on_token_drag)
        self.canvas.tag_bind(self.label, "<ButtonPress-1>", self.on_token_click)
        self.canvas.tag_bind(self.label, "<B1-Motion>", self.on_token_drag)
        self.canvas.tag_bind(self.token, "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind(self.label, "<ButtonRelease-1>", self.on_token_release)

    def on_token_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_token_drag(self, event):
        x, y = event.x - self.start_x, event.y - self.start_y
        self.canvas.move(self.token, x, y)
        self.canvas.move(self.label, x, y)
        self.start_x = event.x
        self.start_y = event.y

    def on_token_release(self, event):
        x, y = event.x - self.start_x, event.y - self.start_y
        self.canvas.coords(self.token, event.x-(event.x%30), event.y-(event.y%30),event.x-(event.x%30)+30,event.y-(event.y%30)+30)
        self.canvas.coords(self.label, event.x-(event.x%30)+15, event.y-(event.y%30)+15)
        self.start_x = event.x
        self.start_y = event.y

    def set_text(self, text):
        self.canvas.itemconfig(self.label, text=text)

    def remove(self):
        self.canvas.delete(self.token)
        self.canvas.delete(self.label)

class ResizingCanvas(Canvas):
    def __init__(self, parent, cell_size, **kwargs):
        self.cell_size = cell_size
        self.rows = 0
        self.cols = 0
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        wscale = int(event.width / self.cell_size)
        hscale = int(event.height / self.cell_size)
        self.width = wscale * self.cell_size
        self.height = hscale * self.cell_size
        self.config(width=self.width, height=self.height)
        self.draw_grid()

    def draw_grid(self):
        self.delete("grid")
        for i in range(0, self.width, self.cell_size):
            self.create_line(i, 0, i, self.height, tags="grid", fill="gray")
        for j in range(0, self.height, self.cell_size):
            self.create_line(0, j, self.width, j, tags="grid", fill="gray")

class TokenGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Token Mozgató Ize")

        self.cell_size = 30
        self.canvas = ResizingCanvas(root, cell_size=self.cell_size, width=850, height=400, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)

        self.tokens = []
        self.create_add_token_button()
        self.create_remove_token_button()
        self.create_background_button()

    def create_add_token_button(self):
        button = tk.Button(self.root, text="Token Hozzáadás", command=self.add_token)
        button.pack()

    def create_remove_token_button(self):
        button = tk.Button(self.root, text="Token Eltávolítás", command=self.remove_token)
        button.pack()

    def create_background_button(self):
        button = tk.Button(self.root, text="Háttér Beállítás", command=self.set_background)
        button.pack()

    def add_token(self):
        x, y = len(self.tokens) * self.cell_size, len(self.tokens) * self.cell_size
        token = Token(self.canvas, x, y)
        token_text = askstring("Token név", "Add meg a token nevét:")
        if token_text is not None:
            token.set_text(token_text)
        self.tokens.append(token)

    def remove_token(self):
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item and ("token" in self.canvas.gettags(item) or "token_label" in self.canvas.gettags(item)):
            self.canvas.unbind("<ButtonPress-1>")
            token_to_remove = self.find_token_by_item(item)
            if token_to_remove and messagebox.askyesno("Törlés", "Biztosan törölni szeretnéd ezt a tokent?"):
                token_to_remove.remove()
                self.tokens.remove(token_to_remove)

    def find_token_by_item(self, item):
        for token in self.tokens:
            if token.token == item[0] or token.label == item[0]:
                return token
        return None

    def set_background(self):
        color = askcolor()[1]
        self.canvas.itemconfig("grid", fill=color)

def main():
    root = tk.Tk()
    game = TokenGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

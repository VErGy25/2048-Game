from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Label, messagebox, simpledialog
from Map_2048 import MapClass
from UI_2048 import UI

root = Tk()                                     # tkinter создание объекта

n = int(simpledialog.askstring(title="2048 Game",
                               prompt="\tGame settings\t\t\n" "\t3 X 3 -> 3 side size",
                               parent=root,
                               initialvalue="4"))
MARGIN = 15                                     # настройки игрового поля
WIDTH = MARGIN * 2 + 400
HEIGHT = MARGIN * 2 + 400
SIDE = ((WIDTH - 2 * MARGIN) / n)-0.6
# размер блоков внутри

UI_size = (MARGIN, WIDTH, HEIGHT, SIDE)

map_ = MapClass(n)                              # создание объекта класса map
UI(parent=root, game=map_, n=n, UI_size=UI_size)                               # создание UI
root.geometry("%dx%d" % (WIDTH, HEIGHT + 150))  # tkinter длина
root.mainloop()                                 # gui запуск
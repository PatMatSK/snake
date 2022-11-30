import tkinter as tk
import random

w = tk.Tk()
w.title("Snake")
score = 0
CANVAS_HEIGH = 300
CANVAS_WIDTH = 300
can = tk.Canvas(w, width=CANVAS_WIDTH, heigh=CANVAS_HEIGH, bg="brown")
can.pack()
lab = tk.Label(w, text=str(score))
lab.pack()


class Snake:
    def __init__(self, my_len):
        self.my_length = my_len
        self.size = 10
        self.body = []
        self.x = CANVAS_WIDTH / 2
        self.y = CANVAS_HEIGH / 2
        self.running = True
        self.fruit = Fruit()
        self.fruit.paint()
        self.cas = 20
        self.possible_cover = 7

    def begin(self):
        for i in range(self.my_length * self.size, 0, -3):
            self.body.append(
                can.create_oval(self.x, self.y + i, self.x + self.size, self.y + i + self.size,
                                fill="green", outline="green"))

    def die(self):
        self.running = False
        can.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGH / 2, text="GAME OVER", fill="RED")
        can.update()

    def right(self, _event=None):
        while self.running:
            self.x += 3
            self.move(3, 0)

    def left(self, _event=None):
        while self.running:
            self.x = self.x - 3
            self.move(-3, 0)

    def up(self, _event=None):
        while self.running:
            self.y = self.y - 3
            self.move(0, -3)

    def down(self, _event=None):
        while self.running:
            self.y += 3
            self.move(0, 3)

    def move(self, x, y):
        can.after(self.cas)

        if 0 < self.x < CANVAS_WIDTH \
            and 0 < self.y < CANVAS_HEIGH \
            and 0 < (self.x + self.size) < CANVAS_WIDTH \
            and 0 < (self.y + self.size) < CANVAS_HEIGH:

            shift_x = (can.coords(self.body[-1])[0] + x) - can.coords(self.body[0])[0]
            shift_y = (can.coords(self.body[-1])[1] + y) - can.coords(self.body[0])[1]

            can.move(self.body[0], shift_x, shift_y)
            self.body.append(self.body.pop(0))
            touch = can.find_overlapping(self.x, self.y, self.x + self.size, self.y + self.size)

            for i in touch:
                if i in self.fruit.show():
                    sign = self.fruit.show().index(i)
                    self.edit(self.fruit.show()[sign + 1])
                    if len(self.fruit.show()) < 3:
                        self.fruit.paint()
                    break
            touch = can.find_overlapping(self.x, self.y, self.x + self.size, self.y + self.size)

            if len(touch) > self.possible_cover:
                self.die()
            can.update()
        else:
            self.die()

    def edit(self, title):
        if title == "j":
            self.cas = 20
            self.grow(10)
            body = 20
        elif title == "p":
            self.grow(5)
            if self.size == 10:
                self.size = 20
                self.get_fat(10)
            body = 10
        elif title == "ch":
            self.grow(3)
            self.cas = 10
            if self.size != 10:
                self.size = 10
                self.get_slim(self.size)
            body = 5
        elif title == "b":
            if self.size != 10:
                self.size = 10
                self.get_slim(self.size)
            self.possible_cover = 1000
            body = 3
        elif title == "l":
            self.grow(5)
            if self.size != 10:
                self.size = 10
                self.get_slim(self.size)
            body = 15

        self.fruit.die((self.fruit.show().index(title)) - 1, body)

    def get_fat(self, size):
        for cast in self.body:
            x1, y1, x2, y2 = can.coords(cast)
            can.coords(cast, x1, y1, x2 + size, y2 + size)
            self.possible_cover = 13

    def get_slim(self, velkost):
        for cast in self.body:
            x1, y1, x2, y2 = can.coords(cast)
            can.coords(cast, x1, y1, x2 - velkost, y2 - velkost)
            self.possible_cover = 7

    def grow(self, count):
        last = can.coords(self.body[0])
        penultimate = can.coords(self.body[1])
        if last[0] == penultimate[0]:
            if last[1] < penultimate[1]:
                kam = [0, -3]
            else:
                kam = [0, 3]
        else:
            if last[0] > penultimate[0]:
                kam = [3, 0]
            else:
                kam = [-3, 0]

        for i in range(count):
            buttom = can.create_oval(last[0] + kam[0], last[1] + kam[1], last[0] + kam[0] + self.size,
                                    last[1] + kam[1] + self.size, fill="green", outline="green")
            self.body.insert(0, buttom)
            last[0] += kam[0]
            last[1] += kam[1]


def find_place():
    x = random.randint(20, CANVAS_WIDTH - 25)
    y = random.randint(20, CANVAS_HEIGH - 25)
    prekr = can.find_overlapping(x, y, x + 10, y + 10)
    while len(prekr) != 0:
        x = random.randint(20, CANVAS_WIDTH - 20)
        y = random.randint(20, CANVAS_WIDTH - 20)
        prekr = can.find_overlapping(x, y, x + 10, y + 10)

    return x, y


class Fruit:
    def __init__(self):
        self.ovocie = []

    def show(self):
        return self.ovocie

    def apple(self, x, y):
        self.ovocie.append(can.create_oval(x, y, x + 10, y + 10, fill="red", outline="red"))
        self.ovocie.append("j")

    def orange(self, x, y):
        self.ovocie.append(can.create_oval(x, y, x + 10, y + 10, fill="orange", outline="orange"))
        self.ovocie.append("p")

    def chilli(self, x, y):
        self.ovocie.append(can.create_arc(x, y, x + 30, y + 30, start=0, extent=45, fill="red", outline="red"))
        self.ovocie.append("ch")

    def berry(self, x, y):
        self.ovocie.append(can.create_oval(x, y, x + 10, y + 10, fill="purple", outline="purple"))
        self.ovocie.append("b")

    def lime(self, x, y):
        self.ovocie.append(can.create_oval(x, y, x + 10, y + 10, fill="lightgreen", outline="lightgreen"))
        self.ovocie.append("l")

    def paint(self):
        x, y = find_place()
        k = random.randint(0, 4)
        if k == 0:
            self.apple(x, y)
        elif k == 1:
            self.chilli(x, y)
        elif k == 2:
            self.orange(x, y)
        elif k == 3:
            self.berry(x, y)
        elif k == 4:
            self.lime(x, y)
        can.update()

    def die(self, ovo, body):
        global score
        score += body
        lab["text"] = score
        can.delete(self.ovocie[ovo])
        self.ovocie.pop(ovo)
        self.ovocie.pop(ovo)
        can.update()
        self.paint()


my_snake = Snake(7)
my_snake.begin()

w.bind('w', my_snake.up)
w.bind('s', my_snake.down)
w.bind("d", my_snake.right)
w.bind('a', my_snake.left)

w.mainloop()

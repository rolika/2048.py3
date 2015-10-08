#2048 game

import random
from tkinter import *
from tkinter import ttk

SIZE = 4 #size of gamefield
NEW = (2, 4) #new value can be 2 or 4
GAMEOVER = "Game Over"

class Data(list):
    """ Values hold in a custom list """
    def __init__(self, size=SIZE):
        super().__init__(['' for i in range(size * size)])
        self.size = size

    def __str__(self):
        """ Console output """
        sep = "+------" * self.size + "+\n"
        empty_sep = "|      " * self.size + "|\n"
        row = "| {: ^4} " * self.size + "|\n"
        field = sep + (empty_sep + row + empty_sep + sep) * self.size
        return field.format(*self)

    def empty(self):
        """ Return list indexes which are empty """
        empty = []
        for i, j in enumerate(self):
            if not j:
                empty.append(i)
        return empty

    def spawn(self):
        """ Add new value at random empty list index """
        new = random.choice(NEW)
        empty = random.choice(self.empty())
        self[empty] = new

    def limits(self, i):
        """ Return field limits to index """
        left_limit = (i // self.size) * self.size
        right_limit = left_limit + self.size
        upper_limit = i - left_limit
        lower_limit = i + (len(self) - 1 - i) // self.size * self.size
        return (left_limit, right_limit, upper_limit, lower_limit)

    def push_left(self):
        """ Push field left """
        for i, value in enumerate(self):
            if value:
                left_limit, right_limit = self.limits(i)[:2]
                for j in range(left_limit, right_limit):
                    if not self[j] and j < i: #first empty place in row
                        self[j] = value
                        self[i] = ''
                        break

    def push_right(self):
        """ Push field right """
        for i in range(len(self) - 1, -1, -1): #from backwards
            if self[i]:
                left_limit, right_limit = self.limits(i)[:2]
                for j in range(right_limit - 1, left_limit, -1):
                    if not self[j] and j > i:
                        self[j] = self[i]
                        self[i] = ''
                        break

    def push_up(self):
        """ Push field up """
        for i, value in enumerate(self):
            if value:
                upper_limit, lower_limit = self.limits(i)[2:]
                for j in range(upper_limit, lower_limit + 1, self.size):
                    if not self[j] and j < i: #first empty place in column
                        self[j] = value
                        self[i] = ''
                        break

    def push_down(self):
        """ Push field down """
        for i in range(len(self) - 1, -1, -1): #from backwards
            if self[i]:
                upper_limit, lower_limit = self.limits(i)[2:]
                for j in range(lower_limit, upper_limit, -self.size):
                    if not self[j] and j > i:
                        self[j] = self[i]
                        self[i] = ''
                        break

    def merge_left(self):
        """ Merge adjacent same values from left """
        score = 0
        for i, value in enumerate(self):
            if value:
                right_limit = self.limits(i)[1]
                if i + 1 < right_limit:
                    if value == self[i + 1]:
                        self[i] *= 2
                        self[i + 1] = ''
                        score += self[i]
        return score


    def merge_right(self):
        """ Merge adjacent same values from right """
        score = 0
        for i in range(len(self) - 1, -1, -1):
            if self[i]:
                left_limit = self.limits(i)[0]
                if i - 1 >= left_limit:
                    if self[i] == self[i - 1]:
                        self[i] *= 2
                        self[i - 1] = ''
                        score += self[i]
        return score

    def merge_up(self):
        """ Merge adjacent same values from top """
        score = 0
        for i, value in enumerate(self):
            if value:
                lower_limit = self.limits(i)[3]
                if i + self.size <= lower_limit:
                    if value == self[i + self.size]:
                        self[i] *= 2
                        self[i + self.size] = ''
                        score += self[i]
        return score

    def merge_down(self):
        """ Merge adjacent same values from bottom """
        score = 0
        for i in range(len(self) - 1, -1, -1):
            if self[i]:
                upper_limit = self.limits(i)[2]
                if i - self.size >= upper_limit:
                    if self[i] == self[i - self.size]:
                        self[i] *= 2
                        self[i - self.size] = ''
                        score += self[i]
        return score

class Game(Frame):
    """ Main game application """
    def __init__(self, root=None):
        super().__init__(root)
        self.init_widgets()
        self.reset()
        self.grid()
        self.bind_all("<Any-KeyPress>", self.keypress)

    def init_widgets(self):
        self.board = StringVar()
        self.highscore, self.score, self.steps = IntVar(), IntVar(), IntVar()
        self.highscore.set("{:0>5}".format(0))
        Label(self, text="Score:", font=("Liberation Mono", "12")).\
            grid(row=0, column=0)
        Label(self, textvariable=self.score, font=("Liberation Mono", "12")).\
            grid(row=0, column=1)
        Label(self, text=" | Steps:", font=("Liberation Mono", "12")).\
            grid(row=0, column=2)
        Label(self, textvariable=self.steps, font=("Liberation Mono", "12")).\
            grid(row=0, column=3)
        Label(self, text=" | High score:", font=("Liberation Mono", "12")).\
            grid(row=0, column=4)
        Label(self, textvariable=self.highscore,
              font=("Liberation Mono", "12")).grid(row=0, column=5)
        Message(self, textvariable=self.board, aspect=100,
                font=("Liberation Mono", "12")).\
                grid(row=1, column=0, columnspan=6)
        ttk.Button(self, text="Reset", command=self.reset).\
                   grid(row=2, column=0, columnspan=6)

    def reset(self):
        self.data = Data()
        self.score.set("{:0>5}".format(0))
        self.steps.set("{:0>5}".format(0))
        self.data.spawn()
        self.board.set(self.data)

    def keypress(self, event):
        self.steps.set("{:0>5}".format(self.steps.get() + 1))
        if event.keysym == "Left":
            self.data.push_left()
            self.score.set("{:0>5}".format(self.score.get() + self.data.merge_left()))
            self.data.push_left()
        elif event.keysym == "Right":
            self.data.push_right()
            self.score.set("{:0>5}".format(self.score.get() + self.data.merge_right()))
            self.data.push_right()
        elif event.keysym == "Up":
            self.data.push_up()
            self.score.set("{:0>5}".format(self.score.get() + self.data.merge_up()))
            self.data.push_up()
        elif event.keysym == "Down":
            self.data.push_down()
            self.score.set("{:0>5}".format(self.score.get() + self.data.merge_down()))
            self.data.push_down()
        if self.score.get() > self.highscore.get():
            self.highscore.set("{:0>5}".format(self.score.get()))
        if self.data.empty():
            self.data.spawn()
            self.board.set(self.data)

def main():
    Game().mainloop()

if __name__ == "__main__":
    main()

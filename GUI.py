import tkinter as tk
from tkinter import messagebox
import transformer
import AStar
import random

try:
    with open("seed.txt") as f:
        random.seed(f.readline())
except Exception:
    random.seed(114514)


class Game:
    # FINAL_STATE = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    FINAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    HARDSHIP = 10000

    def is_eight_digits_can_be_solved(state, final_state):
        def inversion_pairs(state):
            inversions = 0
            for i in range(len(state)):
                for j in range(i + 1, len(state)):
                    if state[i] > state[j]:
                        inversions += 1
            return inversions

        return inversion_pairs(state) % 2 == inversion_pairs(final_state) % 2

    def __init__(self) -> None:
        self.init_state()

    @property
    def state(self):
        return self._state

    @property
    def steps(self):
        return self._steps

    @property
    def estimate_steps(self):
        return self._estiminate_steps

    def require_AI_move(self):
        self._update_ai_result()
        if self._ai_result == None:
            return
        self._state = self._ai_result[0][:]
        self._ai_result.pop(0)
        self._steps += 1

    def init_state(self):
        self._state = []
        self._ai_result = []
        self._ai_need_update = True
        self._steps = 0

        def shuffle_until_okay(state):
            random.shuffle(state)
            while not Game.is_eight_digits_can_be_solved(state, Game.FINAL_STATE):
                random.shuffle(state)

        self._state = Game.FINAL_STATE[:]
        # self._state = [2, 0, 3, 1, 8, 4, 7, 6, 5]
        shuffle_until_okay(self._state)
        self._force_update_ai_result()
        while self._ai_result == None:
            shuffle_until_okay(self._state)
            self._force_update_ai_result()
        self._estiminate_steps = len(self._ai_result)

    def reset_state(self):
        self.init_state()

    def _force_update_ai_result(self):
        self._ai_need_update = True
        self._update_ai_result()

    def _update_ai_result(self):
        if not self._ai_need_update:
            return
        else:
            self._ai_need_update = False
        self._ai_result = AStar.AStar(
            self._state,
            Game.FINAL_STATE,
            transformer.eight_digits,
            transformer.eight_digits_h,
            max_steps=Game.HARDSHIP,
        )
        if self._ai_result != None:
            self._ai_result = self._ai_result[1:]

    def _find_zero_index(self):
        for i in range(9):
            if self._state[i] == 0:
                return i

    def _move_zero(self, shift):
        def swap(l, i, j):
            r = l[:]
            t = r[i]
            r[i] = r[j]
            r[j] = t
            return r

        zero_index = self._find_zero_index()
        zero_new_index = zero_index + shift
        if not (
            zero_index >= 0
            and zero_index < 9
            and zero_new_index >= 0
            and zero_new_index < 9
        ):
            return False
        if (shift == +1 or shift == -1) and (
            zero_index % 3 != zero_new_index % 3 + 1
            and zero_index % 3 != zero_new_index % 3 - 1
        ):
            return False
        self._ai_need_update = True
        self._state = swap(self._state, zero_index, zero_new_index)
        self._steps += 1
        return True

    def move_right(self):
        return self._move_zero(+1)

    def move_left(self):
        return self._move_zero(-1)

    def move_upper(self):
        return self._move_zero(-3)

    def move_down(self):
        return self._move_zero(+3)


## GUI Part


class GUI:
    EMPTY_GRID_BGCOLOR = "hotpink1"
    NONEMPTY_GRID_BGCOLOR = "lightblue3"
    DIGIT_SIZE = 150
    FONT_BUTTON = ("", 12)

    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.geometry(
            f"{ GUI.DIGIT_SIZE * 3 + 100 }x{GUI.DIGIT_SIZE * 3 + 100}+0+0"
        )
        self._root.title("一个八数码小游戏")
        self._current_frame = None
        self._use_playing_frame()

    def mainloop(self):
        self._root.mainloop()

    def _unuse_previous_frame(self):
        if self._current_frame != None:
            # self._current_frame.pack_forget()
            for widget in self._current_frame.winfo_children():
                widget.destroy()
            self._current_frame.destroy()
            self._current_frame = None

    def _use_playing_frame(self):
        self._unuse_previous_frame()

        playing_frame = tk.Frame(self._root)
        playing_frame.bind_all("<Right>", lambda _: self._move_right_button_callback())
        playing_frame.bind_all("<Left>", lambda _: self._move_left_button_callback())
        playing_frame.bind_all("<Down>", lambda _: self._move_down_button_callback())
        playing_frame.bind_all("<Up>", lambda _: self._move_upper_button_callback())
        self._current_frame = playing_frame
        playing_frame.pack()
        self.canvas = tk.Canvas(
            playing_frame, width=3 * GUI.DIGIT_SIZE + 10, height=3 * GUI.DIGIT_SIZE + 10
        )
        self.canvas.pack()
        self.game_object = Game()
        button_frame = tk.Frame(playing_frame)
        button_frame.pack()

        ai_next_step_button = tk.Button(
            button_frame,
            text="让AI走下一步",
            font=GUI.FONT_BUTTON,
            command=self._ai_next_step_callback,
        )
        ai_next_step_button.pack(side="left")
        move_left_button = tk.Button(
            button_frame,
            text="向左走",
            font=GUI.FONT_BUTTON,
            command=self._move_left_button_callback,
        )
        move_left_button.pack(side="left")
        move_right_button = tk.Button(
            button_frame,
            text="向右走",
            font=GUI.FONT_BUTTON,
            command=self._move_right_button_callback,
        )
        move_right_button.pack(side="left")
        move_upper_button = tk.Button(
            button_frame,
            text="向上走",
            font=GUI.FONT_BUTTON,
            command=self._move_upper_button_callback,
        )
        move_upper_button.pack(side="left")
        move_down_button = tk.Button(
            button_frame,
            text="向下走",
            font=GUI.FONT_BUTTON,
            command=self._move_down_button_callback,
        )
        move_down_button.pack(side="left")
        show_helper_info_button = tk.Button(
            button_frame,
            text="帮助",
            font=GUI.FONT_BUTTON,
            command=self._show_helper_info_button_callback,
        )
        show_helper_info_button.pack()

        self._update_playing_frame()

    def _use_winning_frame(self):
        self._unuse_previous_frame()
        self._current_frame = tk.Frame(self._root)
        self._current_frame.pack()
        label = tk.Label(self._current_frame, text="你赢了!", font=("bold", 26))
        label.pack()
        label2 = tk.Label(
            self._current_frame,
            text=f"你的得分是：{self.game_object.steps}, AI可以做到：{self.game_object.estimate_steps}",
        )
        label2.pack()
        buttom_frame = tk.Frame(self._current_frame)
        buttom_frame.pack()
        new_game_button = tk.Button(
            self._current_frame,
            text="重新开始",
            font=GUI.FONT_BUTTON,
            command=self._new_game_button_callback,
        )
        new_game_button.pack()
        exit_button = tk.Button(
            self._current_frame,
            text="退出",
            font=GUI.FONT_BUTTON,
            command=lambda: exit(0),
        )
        exit_button.pack()

    def _update_playing_frame(self):
        self.canvas.delete("all")
        if self.game_object.state == Game.FINAL_STATE:
            self._use_winning_frame()
            return
        for i in range(3):
            for j in range(3):
                x = i * GUI.DIGIT_SIZE
                y = j * GUI.DIGIT_SIZE
                if self.game_object.state[j * 3 + i] == 0:
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + GUI.DIGIT_SIZE,
                        y + GUI.DIGIT_SIZE,
                        fill=GUI.EMPTY_GRID_BGCOLOR,
                    )
                else:
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + GUI.DIGIT_SIZE,
                        y + GUI.DIGIT_SIZE,
                        fill=GUI.NONEMPTY_GRID_BGCOLOR,
                    )
                    self.canvas.create_text(
                        x + GUI.DIGIT_SIZE / 2,
                        y + GUI.DIGIT_SIZE / 2,
                        text=str(self.game_object.state[j * 3 + i]),
                        font=("bold", 18),
                    )

    def _move_left_button_callback(self):
        self.game_object.move_left()
        self._update_playing_frame()

    def _move_right_button_callback(self):
        self.game_object.move_right()
        self._update_playing_frame()

    def _move_down_button_callback(self):
        self.game_object.move_down()
        self._update_playing_frame()

    def _move_upper_button_callback(self):
        self.game_object.move_upper()
        self._update_playing_frame()

    def _ai_next_step_callback(self):
        self.game_object.require_AI_move()
        self._update_playing_frame()

    def _new_game_button_callback(self):
        self.game_object.init_state()
        self._use_playing_frame()

    def _show_helper_info_button_callback(self):
        messagebox.showinfo(
            "帮助",
            "点击下方即可操作，不过我建议使用更加符合人体工学的方法，就是使用方向键。"
            "你可以自己走，也可以让AI帮助你走。本程序使用A*算法。有时会卡一下，这是正常的。"
            "如果点了让AI走没反应，那就是计算时间超了。"
            "你也可以自定义随机种子，方法是在运行目录下面添加seed.txt，里面填入你的随机种子（整数）。"
            "\nDeveloped by Shinonome28@github",
        )


gui = GUI()
gui.mainloop()

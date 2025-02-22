from tkinter import *
from typing_extensions import Literal
from screeninfo import get_monitors

def get_screen_resolution():
    for monitor in get_monitors():
        return (monitor.width, monitor.height)
GSR = get_screen_resolution

class ButtonListbox(Frame):
    def __init__(self, master, buttons, side1: Literal["left", "right", "top", "bottom"] = "top",
                 side2: Literal["left", "right", "top", "bottom"] = "top",
                 fill1: Literal["none", "x", "y", "both"] = 'x',
                 fill2: Literal["none", "x", "y", "both"] = 'y',
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.fill1 = fill1
        self.fill2 = fill2
        self.side1 = side1
        self.side2 = side2

        self.buttons = buttons

        self.create_buttons()

    def create_buttons(self, **kwargs):
        for button in self.buttons:
            button.pack_forget()

        for button in self.buttons:
            button.pack(side=self.side2, fill=self.fill2, pady=10, **kwargs)

    autopack = create_buttons

    def update_buttons(self, new_buttons):
        for button in self.buttons:
            button.pack_forget()
        self.buttons = new_buttons
        self.create_buttons()

def neuro(math_problem: str, user_answer: str, correct_answer: str):
    # Разбиваем математическую проблему на действия и операции
    import re
    actions = re.findall(r'\d+\s*[\+\-\*/\*\*]+\s*\d+', math_problem)
    
    # Перебираем действия и ищем ошибочное действие
    error_action = None
    for index, action in enumerate(actions):
        try:
            # Вычисляем результат текущего действия
            result = eval(action.replace('^', '**'))
            if result == float(correct_answer):
                continue
            elif result == float(user_answer):
                error_action = (action, index + 1)
                break
        except ZeroDivisionError:
            pass
    
    # Определяем название действия и номер
    if error_action:
        operation = re.search(r'[\+\-\*/\*\*]+', error_action[0]).group()
        action_name = {
            '+': 'сложение',
            '-': 'вычитание',
            '*': 'умножение',
            '/': 'деление',
            '**': 'возведение в степень'
        }.get(operation, 'неизвестное действие')
        return (action_name,error_action[1])
    else:
        return ()
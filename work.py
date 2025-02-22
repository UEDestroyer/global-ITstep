import json
import os
import random
import time
import bcrypt
import keyboard
from workSG import *
import secrets  
from tkinter import *
from tkinter import messagebox


JSONFILE = "info.json"
TASKSFILE = "tasks"
SESSIONFILE = "session.json" 

def exit_acc():
    os.remove(SESSIONFILE)
    root.destroy()
    

def generate_math_problem(maxnum: int) -> str:
    problem = ""
    operators = ['+', '-', '*', '/', "**"]
    lst = [-maxnum - 2, maxnum + 2]
    lst.sort()
    num1 = num2 = num3 = 0
    while num1 == 0:
        num1 = random.randint(lst[0], lst[1])
    while num2 == 0:
        num2 = random.randint(lst[0], lst[1])
    while num3 == 0:
        num3 = random.randint(lst[0], lst[1])

    operator1 = random.choice(operators)
    operator2 = random.choice(operators)

    if operator1 == "/" and num2 == 0:
        num2 = random.randint(1, lst[1])
    if operator2 == "/" and num3 == 0:
        num3 = random.randint(1, lst[1])

    if operator1 == "**" or operator2 == "**":
        num1 = num1 % 10
        num2 = num2 % 5
        num3 = num3 % 3

    if operator1 == "**" and operator2 != "**":
        problem = f"({num1} ** {num2}) {operator2} {num3}"
    if operator2 == "**" and operator1 != "**":
        problem = f"{num1} {operator1} ({num2} ** {num3}) "
    elif operator2 == "**" and operator1 == "**":
        problem = f"({num1} {operator1} {num2}) {operator2} {num3}"
    else:
        problem = f"{num1} {operator1} {num2} {operator2} {num3}"
    
    try:
        eval(problem)
    except ZeroDivisionError:
        problem = problem.replace("0",'1')
    except OverflowError:
        problem = generate_math_problem(maxnum)
    
    return problem

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_hash: bytes, user_password: str) -> bool:
    return bcrypt.checkpw(user_password.encode('utf-8'), stored_hash)

def load_users(filename: str) -> dict:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

def save_users(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def save_session(username: str):
    session_data = {
        "user": username,
        "session_token": secrets.token_hex(16) 
    }
    with open(SESSIONFILE, "w", encoding="utf-8") as file:
        json.dump(session_data, file, indent=4)

def load_session() -> dict:
    if os.path.exists(SESSIONFILE):
        with open(SESSIONFILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def change(index0: int, index2: int):
    global nunproblem, index1
    index1 = index2
    lblproblem['text'] = list(tasks[index0]["tasks"].keys())[index2].replace("**", "^")
    nunproblem = round(list(tasks[index0]["tasks"].values())[index2], 2)

def getallerror(strr: str) -> list:
    return [1 if str(error) == strr else 0 for i in range(len(tasks)) for error in tasks[i]["error"]]

def setallerror():
    global tasks, index, index1
    Ptext = f"кол ошибок в + | %: {sum(geterror('+'))} | {int(sum(geterror('+')) / 14 * 100)}%"
    Mtext = f"кол ошибок в - | %: {sum(geterror('-'))} | {int(sum(geterror('-')) / 14 * 100)}%"
    Utext = f"кол ошибок в * | %: {sum(geterror('*'))} | {int(sum(geterror('*')) / 14 * 100)}%"
    Dtext = f"кол ошибок в / | %: {sum(geterror('/'))} | {int(sum(geterror('/')) / 14 * 100)}%"
    Stext = f"кол ошибок в ^ | %: {sum(geterror('**'))} | {int(sum(geterror('**')) / 14 * 100)}%"
    Portext = f"кол ошибок в порядке: {sum(geterror('w'))} | {int(sum(geterror('w')) / 14 * 100)}%"
    lblP1.configure(text=Ptext)
    lblM1.configure(text=Mtext)
    lblU1.configure(text=Utext)
    lblD1.configure(text=Dtext)
    lblS1.configure(text=Stext)
    lblDE1.configure(text=Portext)

def geterror(strr: str) -> list:
    return [1 if str(i) == strr else 0 for i in tasks[index]["error"]]

def setproblem(index5: int):
    global tasks, index, index1
    var = [Button(button_frame, font=("Arial", 20), fg='black',
                  bg="green" if tasks[index5]['completed'][i-1] == 2 else ("gray" if tasks[index5]['completed'][i-1] == 1 else "red"),
                  text="       " + str(i) + "      ",
                  command=lambda i=i: change(index5, i-1))
           for i in range(1, 8)]
    intask_list.update_buttons(var)
    change(index5, 0)
    Ptext = f"кол ошибок в + | %: {sum(geterror('+'))} | {int(sum(geterror('+')) / 14 * 100)}%"
    Mtext = f"кол ошибок в - | %: {sum(geterror('-'))} | {int(sum(geterror('-')) / 14 * 100)}%"
    Utext = f"кол ошибок в * | %: {sum(geterror('*'))} | {int(sum(geterror('*')) / 14 * 100)}%"
    Dtext = f"кол ошибок в / | %: {sum(geterror('/'))} | {int(sum(geterror('/')) / 14 * 100)}%"
    Stext = f"кол ошибок в ^ | %: {sum(geterror('**'))} | {int(sum(geterror('**')) / 14 * 100)}%"
    Portext = f"кол ошибок в порядке: {sum(geterror('w'))} | {int(sum(geterror('w')) / 14 * 100)}%"
    lblP.configure(text=Ptext)
    lblM.configure(text=Mtext)
    lblU.configure(text=Utext)
    lblD.configure(text=Dtext)
    lblS.configure(text=Stext)
    lblDE.configure(text=Portext)

def choose(i):
    global index
    index = i
    setproblem(i)

def enter():
    getter = entrproblem.get()
    if getter != "" and int(tasks[index]["completed"][index1]) == 1:
        if str(nunproblem) == getter or str(nunproblem).replace(".", ',') == getter:
            with open(tasks_filename, "w", encoding='utf-8') as file:
                tasks[index]["completed"][index1] = 2
                if sum([i for i in tasks[index]['completed']]) == 14:
                    tasks[index]["complete"] = 2
                json.dump(tasks, file, indent=4)
            messagebox.showinfo("результат", "Верно")
        else:
            print(nunproblem)
            neu = neuro(list(dict(tasks[index]['tasks']).keys())[index1],
                        float(getter.replace(',', '.')), float(nunproblem))
            with open(tasks_filename, "w", encoding='utf-8') as file:
                tasks[index]["completed"][index1] = 0
                try:
                    tasks[index]["error"][index1] = neu[0]
                except IndexError:
                    tasks[index]["error"][index1] = "w"
                tasks[index]["complete"] = 0
                json.dump(tasks, file, indent=4)
            if neu != ():
                messagebox.showerror("результат", "Неверно\n" + f"Ошибка в {neu[0]}\nДействие номер:{neu[1]}")
            else:
                messagebox.showerror("результат", "Неверно\nОшибка в порядке действий")
    var = [Button(canvas_frame, text="  " * 5 + str(i) + " " * 5,
                  command=lambda i=i: choose(i-1), width=width // 7, height=2,
                  fg='black',
                  bg="green" if tasks[i-1]['complete'] == 2 else ("gray" if tasks[i-1]['complete'] == 1 else "red"))
           for i in range(1, 1001)]
    task_list.update_buttons(var)
    setproblem(index)

def generate_tasks():
    with open(tasks_filename, "w", encoding="utf-8") as file:
        for i in range(1, 1002):
            task_set = {}
            for j in range(7):
                problem = generate_math_problem(i * 100)
                problem_eval = problem.replace("^", "**")
                if "**0" in problem_eval:
                    problem_eval = problem_eval.replace("**0", "*1")
                task_set[problem] = eval(problem_eval)
            tasks.append({"tasks": task_set, "complete": 1, 'completed': [1 for i in range(7)], "user": nunuser, "error": ["" for i in range(7)]})
        json.dump(tasks, file, indent=4)

nunproblem = ""
session_info = load_session()
nunuser = session_info.get("user", "")
index = 0
index1 = 0

if nunuser == "":
    def regist():
        global nunuser
        login = inp.get()
        pw = inp1.get()
        users = load_users(JSONFILE)
        if login in users:
            if verify_password(users[login].encode('utf-8'), pw):
                nunuser = login
                save_session(nunuser)  #сессию
                register.destroy()
                return
            else:
                lbl_status.config(text="Неверный пароль!")
                return
        users[login] = hash_password(pw).decode('utf-8')  #хэш
        save_users(JSONFILE, users)
        nunuser = login
        save_session(nunuser)  # новая сессия
        register.destroy()

    register = Tk()
    register.title("Регистрация / Вход")
    register.geometry('400x200')

    lbl = Label(register, text="Логин:")
    lbl.grid(row=0, column=0, padx=10, pady=10)

    inp = Entry(register)
    inp.grid(row=0, column=1, padx=10, pady=10)

    lbl1 = Label(register, text="Пароль:")
    lbl1.grid(row=1, column=0, padx=10, pady=10)

    inp1 = Entry(register, show="*")
    inp1.grid(row=1, column=1, padx=10, pady=10)

    btn = Button(register, text="Войти / Зарегистрироваться", command=regist)
    btn.grid(row=2, column=0, columnspan=2, pady=10)

    lbl_status = Label(register, text="", fg="red")
    lbl_status.grid(row=3, column=0, columnspan=2)

    register.mainloop()

if nunuser == "":
    exit()

tasks = []
tasks_filename = f"{TASKSFILE}_{nunuser}.json"
if not os.path.isfile(tasks_filename):
    generate_tasks()
else:
    try:
        with open(tasks_filename, encoding="utf-8") as file:
            tasks = json.load(file)
    except json.JSONDecodeError:
        generate_tasks()

def one_to_front():
    window1.lift()

def two_to_front():
    window2.lift()

def three_to_front():
    window3.lift()

def four_to_front():
    window4.lift()

def on_closing():
    root.destroy()

root = Tk()
root.withdraw()

width = GSR()[0] // 2
height = GSR()[1] // 2
geometry = f"{width}x{height}"

window1 = Toplevel(root)
window1.title("Задание")
window1.geometry(geometry)
window1.protocol("WM_DELETE_WINDOW", on_closing)

window2 = Toplevel(root)
window2.title("Выбор")
window2.geometry(geometry)
window2.protocol("WM_DELETE_WINDOW", on_closing)

window3 = Toplevel(root)
window3.title("Диагностика нынешнего задания")
window3.geometry(geometry)
window3.protocol("WM_DELETE_WINDOW", on_closing)

window4 = Toplevel(root)
window4.title("Общая диагностика")
window4.geometry(geometry)
window4.protocol("WM_DELETE_WINDOW", on_closing)


# задание
button_frame = Frame(window1)
button_frame.pack(side=TOP, pady=10, fill=X)

var = [Button(button_frame, font=("Arial", 20), fg='black',
              bg="green" if tasks[0]['completed'][i-1] == 2 else ("gray" if tasks[0]['completed'][i-1] == 1 else "red"),
              text="       " + str(i) + "      ",
              command=lambda i=i: change(0, i-1))
       for i in range(1, 8)]
intask_list = ButtonListbox(button_frame, var, "top", "left", fill2=BOTH)
intask_list.autopack()

lblproblem = Label(window1, text="здесь будет проблема", font=("Arial", 15))
lblproblem.pack()

entrproblem = Entry(window1)
entrproblem.pack(side='top', fill=BOTH, expand=True)

# окно выбора (window2)
canvas = Canvas(window2)
scrollbar = Scrollbar(window2, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

canvas_frame = Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

var = [Button(canvas_frame, text="  " * 5 + str(i) + " " * 5,
              command=lambda i=i: choose(i-1), width=width // 7, height=2,
              fg='black',
              bg="green" if tasks[i-1]['complete'] == 2 else ("gray" if tasks[i-1]['complete'] == 1 else "red"))
       for i in range(1, 1001)]
task_list = ButtonListbox(canvas_frame, var, "top", "top", fill2="x")
task_list.pack(fill=BOTH, expand=True)
canvas_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))


#диагностика

lbldiagnun = Label(window3, text="Диагностика ваших ответов в этом задании", font=("Arial", 35),
                   bg="#e3f2fd", fg="#0d47a1")
lbldiagnun.pack(pady=(20, 10))

lblP = Label(window3, text="кол ошибок в + | %: ", font=("Arial", 30),
             bg="#e3f2fd", fg="#1565c0", padx=10, pady=5)
lblM = Label(window3, text="кол ошибок в - | %: ", font=("Arial", 30),
             bg="#e3f2fd", fg="#1565c0", padx=10, pady=5)
lblU = Label(window3, text="кол ошибок в * | %: ", font=("Arial", 30),
             bg="#e3f2fd", fg="#1565c0", padx=10, pady=5)
lblD = Label(window3, text="кол ошибок в / | %: ", font=("Arial", 30),
             bg="#e3f2fd", fg="#1565c0", padx=10, pady=5)
lblS = Label(window3, text="кол ошибок в ^ | %: ", font=("Arial", 30),
             bg="#e3f2fd", fg="#1565c0", padx=10, pady=5)
lblDE = Label(window3, text="кол ошибок в действиях | %: ", font=("Arial", 30),
              bg="#e3f2fd", fg="#1565c0", padx=10, pady=5)

lblP.pack(fill="x")
lblM.pack(fill="x")
lblU.pack(fill="x")
lblD.pack(fill="x")
lblS.pack(fill="x")
lblDE.pack(fill="x")

# общ диагностик

lbldiagnun_all = Label(window4, text="Общая диагностика ваших ответов", font=("Arial", 35),
                       bg="#e8f5e9", fg="#1b5e20")
lbldiagnun_all.pack(pady=(20, 10))

lblP1 = Label(window4, text="кол ошибок в + | %: ", font=("Arial", 30),
              bg="#e8f5e9", fg="#2e7d32", padx=10, pady=5)
lblM1 = Label(window4, text="кол ошибок в - | %: ", font=("Arial", 30),
              bg="#e8f5e9", fg="#2e7d32", padx=10, pady=5)
lblU1 = Label(window4, text="кол ошибок в * | %: ", font=("Arial", 30),
              bg="#e8f5e9", fg="#2e7d32", padx=10, pady=5)
lblD1 = Label(window4, text="кол ошибок в / | %: ", font=("Arial", 30),
              bg="#e8f5e9", fg="#2e7d32", padx=10, pady=5)
lblS1 = Label(window4, text="кол ошибок в ^ | %: ", font=("Arial", 30),
              bg="#e8f5e9", fg="#2e7d32", padx=10, pady=5)
lblDE1 = Label(window4, text="кол ошибок в действиях | %: ", font=("Arial", 30),
               bg="#e8f5e9", fg="#2e7d32", padx=10, pady=5)

lblP1.pack(fill="x")
lblM1.pack(fill="x")
lblU1.pack(fill="x")
lblD1.pack(fill="x")
lblS1.pack(fill="x")
lblDE1.pack(fill="x")

keyboard.add_hotkey('q', one_to_front)
keyboard.add_hotkey('w', two_to_front)
keyboard.add_hotkey('e', three_to_front)
keyboard.add_hotkey('r', four_to_front)
keyboard.add_hotkey('x', exit_acc)
keyboard.add_hotkey("enter", enter)



window3.configure(bg="#e3f2fd") 
window4.configure(bg="#e8f5e9") 

change(0, 0)
setallerror()
setproblem(0)
root.mainloop()

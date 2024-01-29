from tkinter import *
from datetime import datetime
from tkinter import messagebox
from random import randrange

root = Tk()
root.geometry('872x435+450+215')
root.title('Отчёты об уроках')
root.resizable(False, False)

OPTION_FRAME = LabelFrame(
    root, text="Выберите имя ученика:", padx=140, pady=20, labelanchor='n')
OPTION_FRAME.pack(fill="x")

with open("students list.txt", "r", encoding="utf-8") as file:
    students = []
    for string in file.readlines():
        for el in string.split(","):
            students.append(el.strip())

choice = StringVar()
choice.set(students[0])
drop_menu = OptionMenu(OPTION_FRAME, choice, *students)
drop_menu.pack(side="right", expand=1, fill="x")

option_label = Label(OPTION_FRAME, text="Ученик: ", pady=15, underline=0, width=15)
option_label.pack(side="top")

COMMENT_FRAME = Frame(root)
COMMENT_FRAME.pack(padx=40, pady=10)

entry_label = Label(COMMENT_FRAME, text="Комментарий по уроку: ", pady=20, underline=0)
entry_label.grid(row=2, column=0)

entry = Entry(COMMENT_FRAME, width=40, borderwidth=3)
entry.grid(row=2, column=1, sticky="w")

exclamation_var = IntVar()
exclamation_checkbox = Checkbutton(
    COMMENT_FRAME, text=" ❗  Пометить как важную информацию", variable=exclamation_var)
exclamation_checkbox.grid(row=0, column=0, sticky="w", pady=10, columnspan=2)

heart_var = IntVar()
heart_checkbox = Checkbutton(
    COMMENT_FRAME, text=' ❤️  "Как здорово, что мне за это платят деньги"', variable=heart_var)
heart_checkbox.grid(row=1, column=0, sticky="w", pady=2, columnspan=2)


def exclamation():
    if exclamation_var.get():
        return "❗"
    return ""


def heart():
    if heart_var.get():
        return "❤️"
    return ""


with open("quotes.txt", "r", encoding='utf-8') as quotes:
    quotes_without_spaces = [quote.strip() for quote in quotes.readlines() if quote != "\n"]
    formatted_quotes = []
    for quote in quotes_without_spaces:
        quote = quote.split("(")
        formatted_quotes.append(quote[0] + "\n\n" + "(" + quote[1])


def exit_quotes():
    random_quote_index = randrange(0, len(formatted_quotes))
    messagebox.showinfo("Успешных уроков!", formatted_quotes[random_quote_index])


today = datetime.now()
d, m, y = today.day, today.month, today.year
if len(str(m)) == 1:
    m = "0" + str(m)


def same_date():
    with open(f"{choice.get()}", "r") as the_file:
        lines = [line.strip() for line in the_file.readlines() if line != "\n"]
    global d, m, y
    if f"{d}.{m}.{y}" in lines:
        return True
    return False


def more_feedback_yesno():
    response = messagebox.askyesno("Отчёт успешно отправлен", "Отправить ещё один отчёт?")
    if response:
        input_button["state"] = "normal"
        exclamation_var.set(0), heart_var.set(0)
        entry.delete(0, "end")
    else:
        exit_quotes(), root.quit()


def input_click():
    with open(f"{choice.get()}", "a", encoding='utf-8') as the_file:
        global d, m, y
        comment = heart() + exclamation() + entry.get()
        if comment.strip():
            if same_date():
                the_file.write(f"{comment}\n\n")
            else:
                the_file.write(f"{d}.{m}.{y}\n{comment}\n\n")

            input_button["state"] = "disabled"
            more_feedback_yesno()

        else:
            messagebox.showinfo("Некорректный ввод", 'Заполните поле "Комментарий к уроку"')


def exit_yesno():
    exit_answer = messagebox.askyesno("Уведомление о выходе", "Выйти из программы?")
    if exit_answer:
        exit_quotes(), root.quit()
    else:
        pass


def add_to_students_list(student_name, snd_window, snd_button, end_button):
    with open("students list.txt", "a", encoding="utf-8") as file:
        file.write(", " + student_name)
    snd_button["state"] = "disabled"
    snd_button["text"] = "Готово!"
    end_button["state"] = "normal"


def add_student():
    add_window = Toplevel()
    add_window.attributes("-topmost", True)
    add_window.title("Добавить ученика")
    add_window.geometry("490x190+670+330")

    adding_frame = LabelFrame(add_window, text="Имя нового ученика:", padx=30, pady=10)
    adding_frame.pack()

    add_entry = Entry(adding_frame)
    add_entry.pack(side="right", padx=30, pady=20)
    end_button = Button(add_window, text="Завершить", state="disabled", command=add_window.destroy)
    end_button.place(x=320, y=135)

    add_button = Button(
        adding_frame, text="Добавить",
        command=lambda: add_to_students_list(add_entry.get(), add_window, add_button, end_button))
    add_button.pack(side="right")


button_frame = Frame(root)
button_frame.pack(side="right")

new_student_button = Button(
    button_frame, text="Настройки списка", command=add_student, padx=1, pady=4, width=15)
new_student_button.grid(row=0, column=0)

input_button = Button(COMMENT_FRAME, text="Отправить", command=input_click, padx=12, pady=4)
input_button.grid(row=2, column=2, padx=50, pady=20)

exit_button = Button(button_frame, text="Выход", command=exit_yesno, padx=35, pady=4)
exit_button.grid(row=0, column=1, padx=20, pady=20)

root.mainloop()

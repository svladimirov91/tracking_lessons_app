from tkinter import *
from datetime import datetime
from tkinter import messagebox
from random import randrange

root = Tk()
root.geometry('900x415+335+170')
root.title('Отчёты об уроках')

radio_frame = LabelFrame(
    root, text="Выберите имя ученика и оставьте ваш отчёт об уроке.", padx=20, pady=20)
radio_frame.pack()

option_label = Label(radio_frame, text="Ученик: ", pady=15, underline=0, width=15)
option_label.grid(row=0, column=0)

students = ["Boris",
            "Elizabeth",
            "Каспаров Арнольд",
            "Арсений Кащенко",
            "Никита Лысенко",
            "Дмитрий",
            "Ксения",
            "Илья",
            "Сабина"
            ]
choice = StringVar()
choice.set(students[0])
drop = OptionMenu(radio_frame, choice, *students)
drop.grid(row=0, column=1)

COMMENT_FRAME = Frame(root)
COMMENT_FRAME.pack(pady=10)

entry_label = Label(COMMENT_FRAME, text="Комментарий по уроку: ", pady=20, underline=0)
entry_label.grid(row=0, column=0)

entry = Entry(COMMENT_FRAME, width=40, borderwidth=3)
entry.grid(row=0, column=1, sticky="w")

exclamation_var = IntVar()
exclamation_checkbox = Checkbutton(
    COMMENT_FRAME, text=" ❗  Пометить как важную информацию", variable=exclamation_var)
exclamation_checkbox.grid(row=2, sticky="w", pady=10, columnspan=2)

heart_var = IntVar()
heart_checkbox = Checkbutton(
    COMMENT_FRAME, text=' ❤️  "Как здорово, что мне за это платят деньги"', variable=heart_var)
heart_checkbox.grid(row=3, sticky="w", pady=2, columnspan=2)

today = datetime.now()
d, m, y = today.day, today.month, today.year
if len(str(m)) == 1:
    m = "0" + str(m)

with open("quotes.txt", "r", encoding='utf-8') as quotes:
    quotes_without_spaces = [quote.strip() for quote in quotes.readlines() if quote != "\n"]
    formatted_quotes = []
    for quote in quotes_without_spaces:
        quote = quote.split("(")
        formatted_quotes.append(quote[0] + "\n\n" + "(" + quote[1])


def exit_quotes():
    random_quote_index = randrange(0, len(formatted_quotes))
    messagebox.showinfo("Успешных уроков!", formatted_quotes[random_quote_index])


def exclamation():
    if exclamation_var.get():
        return "❗"
    return ""


def heart():
    if heart_var.get():
        return "❤️"
    return ""


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


button_frame = Frame(root)
button_frame.pack()

input_button = Button(button_frame, text="Отправить", command=input_click, padx=12, pady=4)
input_button.grid(row=0, column=0, padx=20, pady=20)

exit_button = Button(button_frame, text="Выход", command=exit_yesno, padx=20, pady=4)
exit_button.grid(row=0, column=1, padx=20, pady=20)

root.mainloop()

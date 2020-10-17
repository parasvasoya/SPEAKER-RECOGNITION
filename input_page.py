from tkinter import *
from tkinter import filedialog
import os
import shutil


PAGE_HIGHT = 500
PAGE_WIDTH = 650
PATH = r"C:\Users\DC\Documents\wav"
DATA_PATH = r"DATASET"


def open_file1(event):
    global file_name, flag_list
    file1 = filedialog.askopenfilename(initialdir=PATH, title="Select file", filetypes=(("wav files", "*.wav"),))
    if file1 == '':
        return
    if event.widget.cget("text") == 'Choose file1':
        file_name[0].set(file1)
        flag_list[0] = 1
    elif event.widget.cget("text") == 'Choose file2':
        file_name[1].set(file1)
        flag_list[1] = 1
    elif event.widget.cget("text") == 'Choose file3':
        file_name[2].set(file1)
        flag_list[2] = 1
    elif event.widget.cget("text") == 'Choose file4':
        file_name[3].set(file1)
        flag_list[3] = 1
    elif event.widget.cget("text") == 'Choose file5':
        file_name[4].set(file1)
        flag_list[4] = 1


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg, font="Arial 25")
    label.pack(side="top", fill="x", pady=10)
    b1 = Button(popup, text="Okay", font="Arial 15", command=popup.destroy)
    b1.pack(side="top")
    popup.mainloop()


def clear1():
    global user_entry, file_name, name_flag, flag_list, submit1_button
    user_entry.set('')
    name_flag = 0
    for i in file_name:
        i.set(f"select file {file_name.index(i)+1}")
        flag_list[file_name.index(i)] = 0
    submit1_button['state'] = DISABLED


def submit1():
    global user_entry, file_name, root

    set_data_path = os.path.join(DATA_PATH, user_entry.get())
    try:
        os.mkdir(set_data_path)
    except FileExistsError:
        popupmsg("You are alredy registered... ")
        return

    for name, i in zip(file_name, range(1, 6)):
        set_path = os.path.join(set_data_path, f"{user_entry.get()}{i}")
        shutil.copyfile(name.get(), set_path)

    clear1()
    popupmsg("your data submit1ed... ")


def task1():
    global flag_list, submit1_button, name_flag, user_entry
    if user_entry.get() != '':
        name_flag = 1
    if name_flag == 1 and len(set(flag_list)) == 1 and flag_list[0] == 1 and submit1_button["state"] == DISABLED:
        submit1_button["state"] = NORMAL

    root.after(2000, task1)  # reschedule event in 2 seconds


if __name__ == '__main__':
    root = Tk()
    root.geometry(f"{PAGE_WIDTH}x{PAGE_HIGHT}")
    root.title("Home Page")
    user_entry = StringVar(value='')
    name_flag = 0
    file_name = []
    flag_list = []
    for i in range(1, 6):
        flag_list.append(0)
        file_name.append(StringVar(value=f"select file {i}"))

    main_frame = Frame(root, background="gray")

    user_name_label = Label(main_frame, text="User Name : ", font="Arial 25")
    user_name_label.grid(row=0, column=0, padx=10, pady=10)

    user_name_text = Entry(main_frame, textvariable=user_entry, font="Arial 25")
    user_name_text.grid(row=0, column=1, padx=10, pady=10)

    for i in range(1, 6):
        open_file_button = Button(main_frame, text=f"Choose file{i}", font="Arial 17", width=13)
        open_file_button.grid(row=i, column=0, padx=10, pady=10)
        open_file_button.bind("<Button-1>", open_file1)

        file_name_label = Label(main_frame, textvariable=file_name[i-1], font="Arial 12")
        file_name_label.grid(row=i, column=1, padx=10, pady=10, sticky=W)

    submit1_button = Button(main_frame, text="submit1", font="Arial 17", width=13, state=DISABLED, command=submit1)
    submit1_button.grid(row=6, column=0, padx=10, pady=10)

    reset_button = Button(main_frame, text="reset", font="Arial 17", width=13, command=clear1)
    reset_button.grid(row=6, column=1, padx=10, pady=10, sticky=W)

    quit_button = Button(main_frame, text="quit", font="Arial 17", width=13, command=root.destroy)
    quit_button.grid(row=6, column=1, padx=10, pady=10, sticky=E)

    main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)

    root.after(2000, task1)

    root.mainloop()

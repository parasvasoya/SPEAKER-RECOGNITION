from tkinter import *
import os
import pyaudio
import wave
from pydub import AudioSegment
import math
from model_training import train_model
from test_model import test_model
from tqdm import tqdm
import time
import shutil
from tkinter import filedialog


PAGE_HIGHT = 700
PAGE_WIDTH = 1100
PATH = r"C:\Users\DC\Documents\wav"
DATA_PATH = r"DATASET"
SAMPLE_PATH = r"SampleData"
BG = 'cornsilk2'
HBG = "slate gray"
MFBG = "salmon1"
BBG = "azure2"


def record(no):
    global audio_list, test_audio
    ans_audio = []
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 6

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')
    # file_name[no].set('Finished recording')

    # Save the recorded data as a WAV file
    # wf = wave.open(filename, 'wb')
    # wf.setnchannels(channels)
    # wf.setsampwidth(p.get_sample_size(sample_format))
    # wf.setframerate(fs)
    # wf.writeframes(b''.join(frames))
    # wf.close()
    ans_audio.append(channels)
    ans_audio.append(p.get_sample_size(sample_format))
    ans_audio.append(fs)
    ans_audio.append(b''.join(frames))

    if no == 5:
        test_audio = ans_audio.copy()
    else:
        audio_list[no] = ans_audio


def open_file(event):
    global file_name, flag_list, submit_test, test_file_name
    if event.widget.cget("text") == 'Choose file1':
        record(0)
        flag_list[0] = 1
        file_name[0].set('Finished recording')
    elif event.widget.cget("text") == 'Choose file2':
        record(1)
        flag_list[1] = 1
        file_name[1].set('Finished recording')
    elif event.widget.cget("text") == 'Choose file3':
        record(2)
        flag_list[2] = 1
        file_name[2].set('Finished recording')
    elif event.widget.cget("text") == 'Choose file4':
        record(3)
        flag_list[3] = 1
        file_name[3].set('Finished recording')
    elif event.widget.cget("text") == 'Choose file5':
        record(4)
        flag_list[4] = 1
        file_name[4].set('Finished recording')
    if event.widget.cget("text") == 'Choose file':
        record(5)
        test_file_name.set('Finished recording')
        submit_test['state'] = NORMAL


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


def clear():
    global user_entry, file_name, name_flag, flag_list, submit_button, test_file_name, submit_test, result_var
    try:
        user_entry.set('')
        name_flag = 0
        for i in file_name:
            i.set("Wait For Input")
            flag_list[file_name.index(i)] = 0
        test_file_name.set("Wait For Input")
        result_var.set("")
        submit_test['state'] = DISABLED
        submit_button['state'] = DISABLED
    except:
        pass


def clear1():
    global user_entry, file_name, name_flag, flag_list, submit1_button
    user_entry.set('')
    name_flag = 0
    for i in file_name:
        i.set(f"Wait For Input")
        flag_list[file_name.index(i)] = 0
    submit1_button['state'] = DISABLED


def submit():
    global user_entry, file_name, root, audio_list

    set_data_path = os.path.join(DATA_PATH, user_entry.get())
    try:
        os.mkdir(set_data_path)
    except FileExistsError:
        popupmsg("You are alredy registered... ")
        return

    for name, i, audio in zip(file_name, range(1, 6), audio_list):
        set_path = os.path.join(set_data_path, f"{user_entry.get()}{i}.wav")
        wf = wave.open(set_path, 'wb')
        wf.setnchannels(audio[0])
        wf.setsampwidth(audio[1])
        wf.setframerate(audio[2])
        wf.writeframes(audio[3])
        wf.close()

        # Opening file and extracting segment

        song = AudioSegment.from_wav(set_path)
        l = len(list(song))
        # print(l)
        extract = song[l / math.ceil(l / 1000):(l - l / math.ceil(l / 1000))]
        # Saving
        extract.export(set_path, format="wav")

    train_model(user_entry.get())
    for i in tqdm(range(100),
                  desc="Loading…",
                  ascii=False, ncols=100):
        time.sleep(0.1)

    clear()
    popupmsg("your data submited... ")


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

    train_model(user_entry.get())
    for i in tqdm(range(100),
                  desc="Loading…",
                  ascii=False, ncols=100):
        time.sleep(0.1)

    clear1()
    popupmsg("your data submit1ed... ")


def test():
    global test_audio, I, result_var
    set_path = os.path.join(SAMPLE_PATH, f"test{I}.wav")
    wf = wave.open(set_path, 'wb')
    wf.setnchannels(test_audio[0])
    wf.setsampwidth(test_audio[1])
    wf.setframerate(test_audio[2])
    wf.writeframes(test_audio[3])
    wf.close()

    result = test_model(f"test{I}.wav")
    result_var.set(result)

    I += 1


def task():
    global flag_list, submit_button, name_flag, user_entry, flag
    if user_entry.get() != '':
        name_flag = 1
    if name_flag == 1 and len(set(flag_list)) == 1 and flag_list[0] == 1 and submit_button["state"] == DISABLED:
        submit_button["state"] = NORMAL

    root.after(2000, task)  # reschedule event in 2 seconds


def task1():
    global flag_list, submit1_button, name_flag, user_entry
    if user_entry.get() != '':
        name_flag = 1
    if name_flag == 1 and len(set(flag_list)) == 1 and flag_list[0] == 1 and submit1_button["state"] == DISABLED:
        submit1_button["state"] = NORMAL

    root.after(2000, task1)  # reschedule event in 2 seconds


def main_page():
    global main_frame, ragister_frame, test_frame, root, data_frame, ragister_frame1, ragister_frame2
    try:
        ragister_frame.destroy()
    except:
        pass
    try:
        test_frame.destroy()
    except:
        pass
    try:
        data_frame.destroy()
    except:
        pass
    try:
        ragister_frame1.destroy()
    except:
        pass
    try:
        ragister_frame2.destroy()
    except:
        pass

    clear()

    main_frame = Frame(root, background=BG)

    header_frame = Frame(main_frame, background=HBG)

    Label(header_frame, text="SPEAKER - RECOGNITION", background=HBG, font="Arial 30").pack(padx = 10, pady = 10)
    Label(header_frame, text="CONTROL PANEL", background=HBG, font="Arial 30").pack(padx = 10, pady = 10)

    header_frame.pack(fill=X, expand=YES, padx=20, pady=20, anchor=N)

    button_frame = Frame(main_frame, background=BG)
    Button(button_frame, text="Register yourself", font="Arial 17", width=13, background=BBG, command=ragister_page).grid(row=0, column=0, padx=15, pady=20)

    Button(button_frame, text="Test", font="Arial 17", width=13, background=BBG, command=test_page).grid(row=0, column=1, padx=15, pady=20)

    Button(button_frame, text="User Data", font="Arial 17", width=13, background=BBG, command=data_set).grid(row=0, column=2, padx=15, pady=20)

    Button(button_frame, text="Exit", font="Arial 17", width=13, background=BBG, command=root.destroy).grid(row=0, column=3, padx=15, pady=20)

    button_frame.pack(padx=20, pady=200)

    main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)


def ragister_page():
    global main_frame, ragister_frame, user_entry, file_name, submit_button
    try:
        main_frame.destroy()
    except:
        pass


    ragister_frame = Frame(root, background=BG)


    heading_frame = Frame(ragister_frame, background=HBG)
    Label(heading_frame, text="Register Yourself", font="Arial 30", background=HBG).pack(padx=20, pady=20)
    heading_frame.pack(fill=X, expand=YES, padx=20, pady=20, anchor=N)

    main_frame = Frame(ragister_frame, background=BG)

    file_button = Button(main_frame, text="By File", font="Arial 17", width=13, background=BBG, command=ragister_page_file)
    file_button.grid(row=0, column=0, padx=10, pady=10)

    voice_button = Button(main_frame, text="By Voice", font="Arial 17", width=13, background=BBG, command=ragister_page_record)
    voice_button.grid(row=0, column=1, padx=10, pady=10)

    quit_button = Button(main_frame, text="go to home", font="Arial 17", width=13, background=BBG, command=main_page)
    quit_button.grid(row=0, column=2, padx=10, pady=10)

    main_frame.pack(padx=20, pady=200)
    ragister_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)


def ragister_page_record():
    global main_frame, ragister_frame, user_entry, file_name, submit_button, ragister_frame1
    try:
        ragister_frame.destroy()
    except:
        pass

    ragister_frame1 = Frame(root, background=BG)


    heading_frame = Frame(ragister_frame1, background=HBG)
    Label(heading_frame, text="Register Yourself", font="Arial 30", background=HBG).pack(padx=20, pady=20)
    heading_frame.pack(fill=X, expand=YES, padx=20, pady=20, anchor=N)

    main_frame = Frame(ragister_frame1, background=MFBG)

    user_name_label = Label(main_frame, text="User Name : ", font="Arial 25", background=MFBG)
    user_name_label.grid(row=0, column=0, padx=10, pady=10)

    user_name_text = Entry(main_frame, textvariable=user_entry, font="Arial 25")
    user_name_text.grid(row=0, column=1, padx=10, pady=10)

    for i in range(1, 6):
        open_file_button = Button(main_frame, text=f"Choose file{i}", background=BBG, font="Arial 17", width=13)
        open_file_button.grid(row=i, column=0, padx=10, pady=10)
        open_file_button.bind("<Button-1>", open_file)

        file_name_label = Label(main_frame, textvariable=file_name[i-1], font="Arial 12", background=MFBG)
        file_name_label.grid(row=i, column=1, padx=10, pady=10, sticky=W)

    submit_button = Button(main_frame, text="submit", font="Arial 17", width=13, background=BBG, state=DISABLED, command=submit)
    submit_button.grid(row=6, column=0, padx=10, pady=10)

    reset_button = Button(main_frame, text="reset", font="Arial 17", width=13, background=BBG, command=clear)
    reset_button.grid(row=6, column=1, padx=10, pady=10, sticky=W)

    quit_button = Button(main_frame, text="go to home", font="Arial 17", width=13, background=BBG, command=main_page)
    quit_button.grid(row=6, column=1, padx=10, pady=10, sticky=E)

    main_frame.pack(padx=20, pady=20)
    ragister_frame1.pack(fill=BOTH, expand=YES, padx=20, pady=20)
    root.after(2000, task)


def ragister_page_file():
    global main_frame, ragister_frame, user_entry, file_name, submit1_button, ragister_frame2
    try:
        ragister_frame.destroy()
    except:
        pass


    ragister_frame2 = Frame(root, background=BG)


    heading_frame = Frame(ragister_frame2, background=HBG)
    Label(heading_frame, text="Register Yourself", font="Arial 30", background=HBG).pack(padx=20, pady=20)
    heading_frame.pack(fill=X, expand=YES, padx=20, pady=20, anchor=N)

    main_frame = Frame(ragister_frame2, background=MFBG)

    user_name_label = Label(main_frame, text="User Name : ", font="Arial 25", background=MFBG)
    user_name_label.grid(row=0, column=0, padx=10, pady=10)

    user_name_text = Entry(main_frame, textvariable=user_entry, font="Arial 25")
    user_name_text.grid(row=0, column=1, padx=10, pady=10)

    for i in range(1, 6):
        open_file_button = Button(main_frame, text=f"Choose file{i}", background=BBG, font="Arial 17", width=13)
        open_file_button.grid(row=i, column=0, padx=10, pady=10)
        open_file_button.bind("<Button-1>", open_file1)

        file_name_label = Label(main_frame, textvariable=file_name[i - 1], font="Arial 12", background=MFBG)
        file_name_label.grid(row=i, column=1, padx=10, pady=10, sticky=W)

    submit1_button = Button(main_frame, text="submit1", font="Arial 17", width=13, background=BBG, state=DISABLED, command=submit1)
    submit1_button.grid(row=6, column=0, padx=10, pady=10)

    reset_button = Button(main_frame, text="reset", font="Arial 17", width=13, background=BBG, command=clear1)
    reset_button.grid(row=6, column=1, padx=10, pady=10, sticky=W)

    quit_button = Button(main_frame, text="Go to Home", font="Arial 17", width=13, background=BBG, command=main_page)
    quit_button.grid(row=6, column=1, padx=10, pady=10, sticky=E)

    main_frame.pack(padx=20, pady=20)
    ragister_frame2.pack(fill=BOTH, expand=YES, padx=20, pady=20)
    root.after(2000, task1)


def test_page():
    global main_frame, test_frame, submit_test, test_file_name, result_var
    try:
        main_frame.destroy()
    except:
        pass

    test_frame = Frame(root, background=BG)

    heading_frame = Frame(test_frame, background=HBG)
    Label(heading_frame, text="Identify Person", font="Arial 30", background=HBG).pack(padx=20, pady=20)
    heading_frame.pack(fill=X, expand=YES, padx=20, pady=20, anchor=N)

    button_frame = Frame(test_frame, background=BG)

    open_file_button = Button(button_frame, text=f"Choose file", background=BBG, font="Arial 17", width=13)
    open_file_button.grid(row=0, column=0, padx=10, pady=10)
    open_file_button.bind("<Button-1>", open_file)

    file_name_label = Label(button_frame, textvariable=test_file_name, background=BG, font="Arial 12")
    file_name_label.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    submit_test = Button(button_frame, text="Check", font="Arial 17", width=13, background=BBG, state=DISABLED, command=test)
    submit_test.grid(row=1, column=0, padx=10, pady=10)

    reset_button = Button(button_frame, text="reset", font="Arial 17", width=13, background=BBG, command=clear)
    reset_button.grid(row=1, column=1, padx=10, pady=10, sticky=W)

    quit_button = Button(button_frame, text="Go to Home", font="Arial 17", width=13, background=BBG, command=main_page)
    quit_button.grid(row=1, column=2, padx=10, pady=10, sticky=E)

    result_label = Label(button_frame, textvariable=result_var, background=BG, font="Arial 17")
    result_label.grid(row=2, column=1, padx=10, pady=10)

    button_frame.pack(padx=20, pady=150)
    test_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)


def data_set():
    global main_frame, data_frame
    try:
        main_frame.destroy()
    except:
        pass

    data_frame = Frame(root, background=BG)

    heading_frame = Frame(data_frame, background=HBG)
    Label(heading_frame, text="Registered Person", font="Arial 30", background=HBG).pack(padx=20, pady=20)
    heading_frame.pack(fill=X, expand=YES, padx=20, pady=20, anchor=N)

    # Label(data_frame, background=BG).pack(pady=100)

    sub_frame = Frame(data_frame, background="yellow4")

    u_name = os.listdir(DATA_PATH)
    i = j = 0
    for u in u_name:
        if i > 2:
            j += 1
            i = 0
        Label(sub_frame, text=u, background="yellow4", font="Arial 17").grid(row=i, column=j, padx=10, pady=10)
        i += 1
    sub_frame.pack(padx=20, pady=20)

    quit_button = Button(data_frame, text="Go to Home", font="Arial 17", width=13, background=BBG, command=main_page)
    quit_button.pack(padx=10)
    Label(data_frame, background=BG).pack(pady=100)


    data_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)


if __name__ == '__main__':
    root = Tk()
    root.geometry(f"{PAGE_WIDTH}x{PAGE_HIGHT}")
    root.title("Home Page")
    # root.attributes('-fullscreen', True)

    I = len([name for name in os.listdir(SAMPLE_PATH) if os.path.isfile(os.path.join(SAMPLE_PATH, name))]) + 1
    user_entry = StringVar(value='')
    name_flag = 0
    file_name = []
    flag_list = []
    audio_list = []
    test_audio = []
    for i in range(1, 6):
        flag_list.append(0)
        file_name.append(StringVar(value='Wait For Input'))
        audio_list.append([])
    test_file_name = StringVar(value="Wait For Input")
    result_var = StringVar(value="")

    main_page()


    root.mainloop()

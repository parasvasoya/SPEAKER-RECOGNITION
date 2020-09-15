from tkinter import *
import os
import pyaudio
import wave


PAGE_HIGHT = 500
PAGE_WIDTH = 650
PATH = r"C:\Users\DC\Documents"
DATA_PATH = r"DATASET"
SAMPLE_PATH = r"test_samples"


def record(no):
    global audio_list, test_audio
    ans_audio = []
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 1

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


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg, font="Arial 25")
    label.pack(side="top", fill="x", pady=10)
    b1 = Button(popup, text="Okay", font="Arial 15", command=popup.destroy)
    b1.pack(side="top")
    popup.mainloop()


def clear():
    global user_entry, file_name, name_flag, flag_list, submit_button, test_file_name, submit_test
    try:
        user_entry.set('')
        name_flag = 0
        for i in file_name:
            i.set("Recording")
            flag_list[file_name.index(i)] = 0
        test_file_name.set("Recording")
        submit_test['state'] = DISABLED
        submit_button['state'] = DISABLED
    except:
        pass


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

    clear()
    popupmsg("your data submited... ")


def test():
    global test_audio, I
    set_path = os.path.join(SAMPLE_PATH, f"test{I}.wav")
    wf = wave.open(set_path, 'wb')
    wf.setnchannels(test_audio[0])
    wf.setsampwidth(test_audio[1])
    wf.setframerate(test_audio[2])
    wf.writeframes(test_audio[3])
    wf.close()
    I += 1


def task():
    global flag_list, submit_button, name_flag, user_entry, flag
    if user_entry.get() != '':
        name_flag = 1
    if name_flag == 1 and len(set(flag_list)) == 1 and flag_list[0] == 1 and submit_button["state"] == DISABLED:
        submit_button["state"] = NORMAL

    root.after(2000, task)  # reschedule event in 2 seconds


def main_page():
    global main_frame, ragister_frame, test_frame, root
    try:
        ragister_frame.destroy()
    except:
        pass
    try:
        test_frame.destroy()
    except:
        pass
    main_frame = Frame(root, background="brown")

    Button(main_frame, text="Register yourself", font="Arial 17", width=13, command=ragister_page).grid(row=0, column=0, padx=10,
                                                                                               pady=200)

    Button(main_frame, text="Test", font="Arial 17", width=13, command=test_page).grid(row=0, column=1, padx=10)

    Button(main_frame, text="Exit", font="Arial 17", width=13, command=root.destroy).grid(row=0, column=2, padx=10)

    main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)


def ragister_page():
    global main_frame, ragister_frame, user_entry, file_name, submit_button
    try:
        main_frame.destroy()
    except:
        pass

    ragister_frame = Frame(root, background="green")

    user_name_label = Label(ragister_frame, text="User Name : ", font="Arial 25")
    user_name_label.grid(row=0, column=0, padx=10, pady=10)

    user_name_text = Entry(ragister_frame, textvariable=user_entry, font="Arial 25")
    user_name_text.grid(row=0, column=1, padx=10, pady=10)

    for i in range(1, 6):
        open_file_button = Button(ragister_frame, text=f"Choose file{i}", font="Arial 17", width=13)
        open_file_button.grid(row=i, column=0, padx=10, pady=10)
        open_file_button.bind("<Button-1>", open_file)

        file_name_label = Label(ragister_frame, textvariable=file_name[i-1], font="Arial 12")
        file_name_label.grid(row=i, column=1, padx=10, pady=10, sticky=W)

    submit_button = Button(ragister_frame, text="submit", font="Arial 17", width=13, state=DISABLED, command=submit)
    submit_button.grid(row=6, column=0, padx=10, pady=10)

    reset_button = Button(ragister_frame, text="reset", font="Arial 17", width=13, command=clear)
    reset_button.grid(row=6, column=1, padx=10, pady=10, sticky=W)

    quit_button = Button(ragister_frame, text="go to home", font="Arial 17", width=13, command=main_page)
    quit_button.grid(row=6, column=1, padx=10, pady=10, sticky=E)

    ragister_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)


def test_page():
    global main_frame, test_frame, submit_test, test_file_name
    try:
        main_frame.destroy()
    except:
        pass

    test_frame = Frame(root, background="gray")

    open_file_button = Button(test_frame, text=f"Choose file", font="Arial 17", width=13)
    open_file_button.grid(row=i, column=0, padx=10, pady=10)
    open_file_button.bind("<Button-1>", open_file)

    file_name_label = Label(test_frame, textvariable=test_file_name, font="Arial 12")
    file_name_label.grid(row=i, column=1, padx=10, pady=100, sticky=W)

    submit_test = Button(test_frame, text="submit", font="Arial 17", width=13, state=DISABLED, command=test)
    submit_test.grid(row=6, column=0, padx=10, pady=10)

    reset_button = Button(test_frame, text="reset", font="Arial 17", width=13, command=clear)
    reset_button.grid(row=6, column=1, padx=10, pady=10, sticky=W)

    quit_button = Button(test_frame, text="Go to Home", font="Arial 17", width=13, command=main_page)
    quit_button.grid(row=6, column=2, padx=10, pady=10, sticky=E)

    test_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)


if __name__ == '__main__':
    root = Tk()
    root.geometry(f"{PAGE_WIDTH}x{PAGE_HIGHT}")
    root.title("Home Page")

    I = len([name for name in os.listdir(SAMPLE_PATH) if os.path.isfile(os.path.join(SAMPLE_PATH, name))]) + 1
    user_entry = StringVar(value='')
    name_flag = 0
    file_name = []
    flag_list = []
    audio_list = []
    test_audio = []
    for i in range(1, 6):
        flag_list.append(0)
        file_name.append(StringVar(value='Recording'))
        audio_list.append([])
    test_file_name = StringVar(value="recording")

    main_page()

    root.after(2000, task)

    root.mainloop()

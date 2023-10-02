import threading
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk
from pytube import YouTube

window_width = 800
window_height = 500


def progress_callback(stream, chunk, bytes_remaining):
    size = video.filesize
    progress = int(((size - bytes_remaining) / size) * 100)
    pb['value'] = progress
    perc.config(text=str(progress) + " %")


def complete_callback(stream, file_handle):
    frame_convert.pack()
    frame_download.pack_forget()
    showinfo(message='Download Completed!')


def handle_converter():
    global video
    global ent_url

    url = ent_url.get()
    yt = YouTube(url)
    yt.register_on_progress_callback(progress_callback)
    yt.register_on_complete_callback(complete_callback)
    mp4_files = yt.streams.filter(file_extension="mp4")
    video = mp4_files.get_highest_resolution()
    if video is not None:
        print("Video found:", video)
    else:
        print("No suitable video stream found.")
    frame_convert.pack_forget()
    frame_download.pack()


def download_thread():
    video.download()


def handle_download():
    if video is not None:
        threading.Thread(target=download_thread).start()


if __name__ == "__main__":
    window = tk.Tk()
    def_font = ("Montserrat", 12)
    window.option_add("*Font", def_font)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2.3 - window_height / 2.3)

    image = Image.open("blue_logo.jpg")

    window.iconphoto(False, ImageTk.PhotoImage(image))
    window.title("Youtube Converter")
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    frame1 = tk.Frame(master=window, width=150, height=250)
    frame1.pack()
    image = Image.open("logo.jpg").resize((150, 150))
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(frame1, image=photo)
    label.pack(expand=True)
    label.place(relx=0.5, rely=0.5, anchor="center")

    frame_convert = tk.Frame(master=window, width=300, height=300)
    frame_convert.pack()

    frame_download = tk.Frame(master=window, width=300, height=300)

    perc = tk.Label(master=frame_download, text="")
    perc.place(relx=0.5, rely=0.3, anchor="center")

    pb = ttk.Progressbar(frame_download, orient='horizontal', mode="determinate", length=280)
    pb.place(relx=0.5, rely=0.2, anchor="center")

    ent_url = tk.Entry(master=frame_convert)
    ent_url.pack()
    ent_url.place(relx=0.5, rely=0.2, anchor="center")

    btn_convert = tk.Button(frame_convert, text="Converter", command=handle_converter)
    btn_convert.pack()
    btn_convert.place(relx=0.5, rely=0.5, anchor="center")

    btn_download = tk.Button(frame_download, text="Download", command=handle_download)
    btn_download.pack()
    btn_download.place(relx=0.5, rely=0.5, anchor="center")

    window.mainloop()

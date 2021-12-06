import threading
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pytube import Playlist
from pytube.__main__ import YouTube
from pytube.request import stream
import urllib.request
from PIL import ImageTk, Image


def set_window():
    # configuring up the window layout and position
    root.title("YouTube Video Downloader")
    # icon = PhotoImage(file='./1002.png')
    # window.iconphoto(True, icon)
    window_width = 700
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


root = Tk()
set_window()
# Start Scrollbar
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(
    main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
    scrollregion=my_canvas.bbox("all")))
second_frame = Frame(my_canvas)
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
# End Scrollbar





def fetch_info():
    playlist_link = video_link_entry.get()
    playlist = Playlist(playlist_link)
    i = 1
    global var
    k = 0
    global services
    services = []
    for video in playlist.videos:
        Label(second_frame, text=f"Video {i}").grid()

        # urllib.request.urlretrieve(  # nosec
        #     video.thumbnail_url, "video1_thumbnail.png")  # nosec
        # image = Image.open("video1_thumbnail.png")
        # img = image.resize((50, 50))
        # my_img = ImageTk.PhotoImage(img)
        # my_label_img = Label(second_frame, image=my_img)
        # my_label_img.grid()
        
        Label(second_frame, text=f"Title: {video.title[0:50]}").grid()
        fetch_quality_info(video.embed_url)
        Label(second_frame, text=" ".join(str(x)
              for x in available_res)).grid()
        Label(second_frame, text=" ".join(str(x) for x in sizes)).grid()
        for res in available_res:
            option = IntVar()
            option.set(0)
            services.append(option)
            Checkbutton(second_frame, text=f"Download {res}",
                        variable=services[k]).grid()
            k += 1
        Label(second_frame, text="-"*60).grid()
        i += 1

    download_button2 = Button(
        second_frame,
        text="Download Checked Videos",
        bg="red",
        fg="white", command=lambda: threading.Thread(target=download_video).start())
    download_button2.grid(row=1, column=2)
    Button(second_frame, text="Submit Selections",
           command=show).grid(row=2, column=2)


def show():
    global selected
    global ls
    ls = []
    for i in range(len(services)):
        selected = ""
        if services[i].get() >= 1:
            selected += str(i)
            ls.append(str(i))
            print(selected)


def download_video():
    url = video_link_entry.get()
    playlist = Playlist(url)
    global stream_lst
    stream_lst = []
    urls = []
    for video in playlist.videos:
        urls.append(video.embed_url)
    j = 0
    for video in playlist.videos:
        for i in available_res:
            v = YouTube(urls[j], on_progress_callback=on_progress)
            stream = v.streams.filter(
                progressive=True).get_by_resolution(i)
            stream_lst.append(stream)
        j += 1
    print(stream_lst)
    for i in ls:
        stream_lst[int(i)].download(folder_name)


def on_progress(chunk: bytes, file_handler, bytes_remaining: int):
    global my_label
    count = 1
    for i in stream_lst:
        bytes_downloaded = i.filesize-bytes_remaining
        # print(i.filesize)
        # `print(i.filesize-bytes_remaining)
        progress2 = (bytes_downloaded/i.filesize)*100
        progress.set(f"progress {count}: "+str(round(progress2))+"%")
        #my_label = Label(second_frame, text=f"progress {progress}%")
        # my_label.grid()
        second_frame.update_idletasks()
        count += 1
        break




def open_save_location():
    """This function opens a folder browser to choose where to save your video or playlist"""
    global folder_name
    folder_name = filedialog.askdirectory()
    folder_name_print = Label(second_frame, text="Save to "+folder_name)
    folder_name_print.grid(row=3, column=0)




def fetch_quality_info(video_link):
    global sizes
    global available_res
    video = YouTube(video_link)
    available_res = []
    stream = video.streams.filter(
        progressive=True).get_by_resolution("720p")
    if(stream != None):
        available_res.append("720p")
    stream = video.streams.filter(
        progressive=True).get_by_resolution("480p")
    if(stream != None):
        available_res.append("480p")
    stream = video.streams.filter(
        progressive=True).get_by_resolution("360p")
    if(stream != None):
        available_res.append("360p")
    stream = video.streams.filter(
        progressive=True).get_by_resolution("144p")
    if(stream != None):
        available_res.append("144p")
    sizes = []
    for i in available_res:
        stream = video.streams.filter(
            progressive=True).get_by_resolution(i)
        if(stream != None):
            sizes.append(str(round(stream.filesize/(1024*1024)))+" MB")


Label(second_frame, text="Enter playlist URL").grid(
    row=0, column=0, columnspan=2)
video_link_entry = Entry(second_frame, width=50, borderwidth=1)
video_link_entry.grid(row=1, column=0, padx=10, pady=10)

submit_url_button = Button(second_frame, text="Submit Link", bg="white",
                           fg="black", command=lambda: threading.Thread(target=fetch_info).start())
submit_url_button.grid(row=1, column=1)

progress = StringVar()
progress.set("progress: ")
my_label = Label(second_frame, textvariable=progress).grid()

choose_location = Button(
    second_frame,
    text="Choose save location",
    bg="white",
    fg="black",
    command=open_save_location,
)
choose_location.grid(row=3, column=1)

root.mainloop()

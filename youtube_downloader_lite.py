from pytube import YouTube
from time import sleep
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess



window = tk.Tk()
window.title("Youtube Downloader")
window.geometry("400x400")

notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

path = ""
file_path = ""

try:
    with open('data/path.txt', 'r') as f:
        path = f.read()
except:
    path = os.path.join(os.path.expanduser("~"), "Videos/yt_dl")
    if os.path.exists(path) == False: path = "myVids"

def save_path(new_path):
    global path
    path = new_path
    with open('data/path.txt', 'w') as f:
        f.write(new_path)


#///////////////////////////////// VIDEO DOWNLOAD FUNCTION ///////////////////////////////
def start_download(url,res):
    try:
        yt = YouTube(url)
        if(res!=""):
            try:
                stream = yt.streams.filter(file_extension='mp4',res=res).first()
            except:
                download_status.config(text="ERROR\nEither you entered a resolution that doesn't exist, or there was an issue downloading the video.\nTry again with no resolution specified.")
        else:
            stream = yt.streams.get_highest_resolution()
        try:
            stream.download(output_path=path)
            download_status.config(text=f'Downloaded "{yt.title}"')
            global file_path
            file_path = path + '/' + yt.title + '.mp4'
            subprocess.Popen(f'explorer /select,"{os.path.realpath(file_path)}"')
        except Exception as e:
            print(e)
            download_status.config(text="ERROR\nUnable to download")
    except:
        download_status.config(text='invalid url, ensure you pasted it correctly')




#///////////////////////////////// AUDIO DOWNLOAD FUNCTION ///////////////////////////////

def start_download_audio(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        try:
            stream.download(output_path=path)
            download_status_a.config(text=f'Downloaded "{yt.title}"')
        except:
            download_status_a.config(text='unable to download.')
    except Exception as e:
        download_status_a.config(text='invalid url, ensure you pasted it correctly')

notebook.add(tab1, text="Video")
notebook.add(tab2, text="Audio")

video_link = tk.Label(tab1, text="\nPaste Video Link:")
video_link.pack()

video_link_entry = tk.Entry(tab1,width=40)
video_link_entry.pack()

sel_res_text = tk.Label(tab1, text="\n\nType Desired Resolution\nEx:720p\nLeave blank for the highest SD video available:")
sel_res_text.pack()

sel_res_entry = tk.Entry(tab1)
sel_res_entry.pack()

space1 = tk.Label(tab1, text="\n")
space1.pack()

download_button = tk.Button(tab1, text="\n    Download    \n", command=lambda:start_download(video_link_entry.get(),sel_res_entry.get()))
download_button.pack()
download_button.configure(bg='#6cd929',fg='black')

download_status = tk.Label(tab1, text="")
download_status.pack()

#////////////////////////////////////////////////////////// AUDIO ////////////////////////////////////////////////////////////

audio_link = tk.Label(tab2, text="\nPaste Video Link:")
audio_link.pack()

audio_link_entry = tk.Entry(tab2,width=40)
audio_link_entry.pack()

space1 = tk.Label(tab2, text="\n\n")
space1.pack()

download_button_a = tk.Button(tab2, text="\n    Download    \n", command=lambda:start_download_audio(audio_link_entry.get()))
download_button_a.pack()
download_button_a.configure(bg='#6cd929',fg='black')

download_status_a = tk.Label(tab2, text="")
download_status_a.pack()




window.iconbitmap("data/icon.ico")

window.mainloop()
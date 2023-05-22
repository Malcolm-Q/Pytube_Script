from pytube import YouTube
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from moviepy.editor import VideoFileClip
import os
import cv2
import subprocess



window = tk.Tk()
window.title("Youtube Downloader")
window.geometry("500x600")

notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)

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
            disclaimer.config(text=f"Loaded Downloaded Video:\n{file_path}")
        except Exception as e:
            print(e)
            download_status.config(text="ERROR\nUnable to download or you provided an incorrect path.\nExample path: C:/Users/<user>/Videos")
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

def clip(file, start, end):
    file = os.path.join(path,file)
    try: loaded_video = VideoFileClip(file)
    except: disclaimer.config(text="Error accessing file")

    if(start == "" and end == ""):
        disclaimer.config(text="Assign a value to start and/or end before clipping...")
        return

    if(start == ""): start = 0
    if(end == ""): end = loaded_video.duration

    try: loaded_video = loaded_video.subclip(int(start),int(end))
    except: disclaimer.config(text="Error clipping file")

    try: 
        loaded_video.write_videofile(os.path.join(path,"clippedVideo.mp4"), fps=30,codec='libx264',audio_codec = "aac")
        disclaimer.config(text="Done!")
    except: disclaimer.config(text="Error writing file.")


#///////////////////////////////// COMPRESSION FUNCTIONS ///////////////////////////////

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(initialdir=os.path.realpath(path))
    disclaimer.config(text=f"Selected File:\n{file_path}")

def change_res(file,w,h):
    file = os.path.join(path,file)
    try:
        loaded_video = VideoFileClip(file)
    except:
        disclaimer.config(text="Error with file")
    try:
        loaded_video = loaded_video.resize((int(w),int(h)))
        loaded_video.write_videofile(os.path.join(path,"compressedVideo.mp4"), fps=30,codec='libx264',audio_codec = "aac")
        disclaimer.config(text="Done!")
    except Exception as e:
        disclaimer.config(text="Error writing file.")

def get_stats(file):
    file = os.path.join(path,file)
    try:
        loaded_video = VideoFileClip(file)
    except:
        disclaimer.config(text="Error with file")
    duration = loaded_video.duration
    size = loaded_video.size
    bitrate = int(os.path.getsize(file) / (duration * 170))
    filesize = os.path.getsize(file) / (1024 * 1024)
    disclaimer.config(text=f"Duration: {duration} seconds,\nResolution: {size[0]} x {size[1]},\nBitrate: ~{bitrate} kbps,\nFilesize: {filesize} MB.")

def change_bitrate(file,mb):
    file = os.path.join(path,file)
    try:
        loaded_video = VideoFileClip(file)
    except:
        disclaimer.config(text="Error with file")
    try:
        mb = int(mb)
        bitrate = ((mb * 8 * 1024) / loaded_video.duration) * 0.75
        loaded_video.write_videofile(os.path.join(path,"compressedVideo.mp4"), fps=30,codec='libx264',bitrate=str(int(bitrate))+'k')
        disclaimer.config(text="Done!")
    except:
        disclaimer.config(text="Failed to compress. Try again..")

notebook.add(tab1, text="Video")
notebook.add(tab2, text="Audio")
notebook.add(tab3, text="Compression")
notebook.add(tab4, text="Set Path")

video_link = tk.Label(tab1, text="\nPaste Video Link:")
video_link.pack()

video_link_entry = tk.Entry(tab1,width=40)
video_link_entry.pack()

sel_res_text = tk.Label(tab1, text="\n\nType Desired Resolution\nEx:720p\nLeave blank for the highest SD video available:")
sel_res_text.pack()

sel_res_entry = tk.Entry(tab1)
sel_res_entry.pack()

space1 = tk.Label(tab1, text="\n\n")
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

#////////////////////////////////////////////////////////// COMPRESSION ////////////////////////////////////////////////////////////


disclaimer = tk.Label(tab3, text="Long videos can take a while to write!")
disclaimer.pack()

open_button = tk.Button(tab3, text="\n         Open Video         \n", command=open_file)
open_button.pack()

space = tk.Label(tab3, text="\n")
space.pack()

stats = tk.Button(tab3, text="Check Stats!", command=lambda:get_stats(file_path))
stats.pack()

res_width = tk.Label(tab3, text="\n\nEnter new WIDTH of video (in pixels):")
res_width.pack()

w_entry = tk.Entry(tab3)
w_entry.pack()

res_height = tk.Label(tab3, text="Enter new HEIGHT of video (in pixels):")
res_height.pack()

h_entry = tk.Entry(tab3)
h_entry.pack()

res_change = tk.Button(tab3, text="Change Resolution", command=lambda:change_res(file_path,w_entry.get(),h_entry.get()))
res_change.pack()

bit_reduct = tk.Label(tab3, text="\n\nEnter target size in MB (bitrate reduction):")
bit_reduct.pack()

mb_entry = tk.Entry(tab3)
mb_entry.pack()

bitrate_change = tk.Button(tab3, text="Change Bitrate", command=lambda:change_bitrate(file_path,mb_entry.get()))
bitrate_change.pack()

start_disc = tk.Label(tab3, text="\n\nEnter the START of the video (seconds)\nLeave empty for 0:")
start_disc.pack()

start_entry = tk.Entry(tab3)
start_entry.pack()

end_disc = tk.Label(tab3, text="Enter new END of the video (seconds)\nLeave empty for video duration:")
end_disc.pack()

end_entry = tk.Entry(tab3)
end_entry.pack()

try_clip = tk.Button(tab3, text="Clip Video", command=lambda:clip(file_path,start_entry.get(),end_entry.get()))
try_clip.pack()

path_name = tk.Label(tab4, text="\nEnter desired path to save videos to (leave blank to download by the .exe):")
path_name.pack()

path_entry = tk.Entry(tab4)
path_entry.pack()

bitrate_change = tk.Button(tab4, text="Save Path", command=lambda:save_path(path_entry.get()))
bitrate_change.pack()

path_entry.insert(0,path)

window.iconbitmap("data/icon.ico")

window.mainloop()
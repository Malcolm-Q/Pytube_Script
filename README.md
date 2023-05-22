# Pytube_Script
A quick and ugly looking program I made for my friends to safely download YouTube videos or audio and learn TKinter.

Do you hate using the ever changing malicious and/or invasive YouTube video audio downloader websites? Here's a very simple program to put those days behind you.

Saves videos to `C:/users/{user}/Videos/yt_dl` by default.

pytube, TKinter, and MoviePy.

Contains a full version and a lite version.

Full Version:
* Bitrate Compression
* Resolution Resizing
* Download Audio
* Download Video (any quality)
* Custom Save Path

Lite Version:
* Download Audio
* Download Video (any quality)

**NOTE:**
```
pyinstaller --onefile --noconsole .\youtube_downloader.py
``` 
will make a ~300mb distributable .exe

```
pyinstaller --onefile --noconsole .\youtube_downloader_lite.py
``` 
will make a ~10mb distributable .exe

Alternatively you can just run the script of course:
```
python youtube_downloader.py
```

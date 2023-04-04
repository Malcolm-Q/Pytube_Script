from pytube import YouTube
from time import sleep
type = input('Download audio ("a"), or video ("v")?: ').lower()
if type == 'v':
    url = input("Paste the URL of the YouTube video to download: ")
    try:
        yt = YouTube(url)
        permission = input(f'URL leads to "{yt.title}" do you want to download it? (y/n)').lower()
        if permission == 'y':
            res = input("pick resolution (720p,480p,etc). Leave empty for highest available: ")
            file = input("pick file extension (mp4,webm,3gp). Leave empty for mp4: ")
            if res != '' or file != '':
                try:
                    stream = yt.streams.filter(file_extension='mp4', res='720p').first()
                except:
                    print('format not available or understood (does the video support that option?)')
            else:
                stream = yt.streams.get_highest_resolution()
            try:
                stream.download()
                print(f'Downloaded "{yt.title}"')
                sleep(3)
            except:
                print('unable to download\ntry another format / default settings?')
                sleep(3)
        else:
            print('download cancelled')
            sleep(2)
    except:
        print('invalid url, ensure you pasted it correctly')
else:
    url = input("Paste the URL of the YouTube video to download: ")
    try:
        yt = YouTube(url)
        permission = input(f'URL lead to "{yt.title}" do you want to download it? (y/n)').lower()
        if permission == 'y':
            stream = yt.streams.filter(only_audio=True).first()
            try:
                stream.download()
                print(f'Downloaded "{yt.title}"')
                sleep(3)
            except:
                print('unable to download\ntry another format / default settings?')
                sleep(3)
        else:
            print('download cancelled')
            sleep(2)
    except:
        print('invalid url, ensure you pasted it correctly')
        sleep(2)
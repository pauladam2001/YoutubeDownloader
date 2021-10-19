from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk     # for combo box
from pytube import YouTube  # for downloading youtube videos
from win10toast import ToastNotifier    # for notification on screen


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Youtube Downloader")
        self.root.iconbitmap("../YoutubeVideoDownloader/download_icon.ico")
        self.root.config(bg='white')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # make the main window pop on the middle of the screen
        y = (screen_height / 2) - (300 / 2)
        self.root.geometry(f'{500}x{300}+{int(x)}+{int(y)}')

        self.root.columnconfigure(0, weight=1)     # set all content in center

        self.folder_name = ''

        self.toaster = ToastNotifier()

    def set_artist_song(self, arg):
        try:
            youtube = YouTube(self.url_entry.get())
            video = youtube.streams.first()
            self.artist_song_label.config(text=video.title)
        except Exception:
            messagebox.showerror('Error', 'Introduce a valid URL!')
            self.url_entry.delete(0, END)

    def download_location(self):
        self.folder_name = filedialog.askdirectory()
        if self.folder_name == '':
            messagebox.showerror('Error', 'Please choose a location!')

    def download_video(self):
        choice = self.choices_box.get()
        url = self.url_entry.get()

        if self.folder_name == '':
            messagebox.showerror('Error', 'Please choose a location!')
        else:
            try:
                if len(url) > 0:
                    youtube = YouTube(url)
                    if choice == self.choices[0]:
                        video = youtube.streams.filter(progressive=True).get_highest_resolution()
                    elif choice == self.choices[1]:     # 720p
                        video = youtube.streams.filter(progressive=True).get_lowest_resolution()
                    elif choice == self.choices[2]:     # Audio Only
                        video = youtube.streams.filter(only_audio=True).first()
                    else:
                        messagebox.showerror('Error', 'Choose video quality!')

                    video.download(self.folder_name)

                    self.toaster.show_toast('Download completed!', 'Your video was downloaded!',
                                            icon_path="../YoutubeVideoDownloader/check_icon.ico", duration=5, threaded=True)    # otherwise the window will freeze
                else:
                    messagebox.showerror('Error', 'Insert a valid video URL!')
            except Exception:
                self.toaster.show_toast('Download failed!', 'Your video was not downloaded!',
                                        icon_path="../YoutubeVideoDownloader/wrong_icon.ico", duration=5, threaded=True)
        self.url_entry.delete(0, END)
        self.choices_box.set('')
        self.folder_name = ''

    def start(self):
        url_label = Label(self.root, text='Paste here a valid video URL', font=('Cooper Black', 15), bg='white')
        url_label.grid()

        self.url_entry = Entry(self.root, width=50, border=2, font=('Cooper Black', 10))
        self.url_entry.grid()
        self.url_entry.bind('<Return>', self.set_artist_song)

        self.artist_song_label = Label(self.root, text='', bg='white', fg='black', font=('Cooper Black', 10))
        self.artist_song_label.grid(pady=10)

        path_button = Button(self.root, width=25, bg='blue', fg='white', text='Choose download path', font=('Cooper Black', 10), command=self.download_location)
        path_button.grid(pady=20)

        quality_label = Label(self.root, text='Select quality', bg='white', font=('Cooper Black', 15))
        quality_label.grid()

        self.choices = ['High resolution', 'Low resolution', 'Audio Only']
        self.choices_box = ttk.Combobox(self.root, values=self.choices, font=('Cooper Black', 10))
        self.choices_box.grid()

        download_button = Button(self.root, width=15, bg='blue', fg='white', text='Download', font=('Cooper black', 10), command=self.download_video)
        download_button.grid(pady=40)

        self.root.mainloop()

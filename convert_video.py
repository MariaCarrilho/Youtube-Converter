import threading


class ThreadDownload(threading.Thread):
    def __init__(self, video):
        threading.Thread.__init__(self)
        self.video = video

    def run(self):
        try:
            self.video.download()
        except Exception as e:
            print(f"Error: {e}")
            print("Can't convert video")

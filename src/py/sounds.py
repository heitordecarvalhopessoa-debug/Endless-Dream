import winsound
import threading

class Sounds:
    def __init__(self):
        pass

    def play_collect(self):
        threading.Thread(target=lambda: winsound.Beep(880, 120)).start()

    def play_damage(self):
        threading.Thread(target=lambda: winsound.Beep(220, 150)).start()
from threading import Lock

class ConcurrencyControl:
    def __init__(self):
        self.lock = Lock()

    def acquire_lock(self):
        self.lock.acquire()

    def release_lock(self):
        self.lock.release()
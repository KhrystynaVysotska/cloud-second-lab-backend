import queue

from sse.utils import format_sse


class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=1000)
        self.listeners.append(q)
        self.listeners[len(self.listeners) - 1].put_nowait(format_sse(data="You have successfully connected."))
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]
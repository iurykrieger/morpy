from multiprocessing import Process
import abc


class AbstractProcess(object):
    def __init__(self):
        self.process = Process(target=self.run, args=())
        self.process.daemon = True  # Daemonize it

    @abc.abstractmethod
    def run(self):
        return

    def start(self):
        self.process.start()

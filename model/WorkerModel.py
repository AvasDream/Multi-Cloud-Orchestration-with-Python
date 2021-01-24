from utils.utility import init_logging


class Worker():
    def __init__(self,worker_name, worker_size, worker_ip, created_at):
        self.name = worker_name
        self.size = worker_size
        self.ip = worker_ip
        self.created_at = created_at
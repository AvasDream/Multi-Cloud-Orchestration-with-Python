from abc import ABC, abstractmethod

class CloudStrategy(ABC):
    
    @abstractmethod
    def create_worker(self, worker_name=None):
        pass

    @abstractmethod
    def delete_worker(self, worker_name):
        pass

    @abstractmethod
    def delete_all_workers(self):
        pass

    @abstractmethod
    def get_all_workers(self):
        pass

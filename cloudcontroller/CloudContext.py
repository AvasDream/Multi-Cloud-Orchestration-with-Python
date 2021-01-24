from abc import ABC, abstractmethod



class CloudContext():
    """
    The Context defines the cloud interface of interest to the view layer.
    """

    def __init__(self, CloudStrategy):
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._CloudStrategy = CloudStrategy

    @property
    def CloudStrategy(self):
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """
        return self._CloudStrategy

    @CloudStrategy.setter
    def CloudStrategy(self, CloudStrategy):
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """
        self._CloudStrategy = CloudStrategy

    def create_worker(self, worker_name=None):
        return self._CloudStrategy.create_worker(worker_name)

    def delete_worker(self, worker_name):
        return self._CloudStrategy.delete_worker(worker_name)

    def delete_all_workers(self):
        return self._CloudStrategy.delete_all_workers()

    def get_all_workers(self):
        return self._CloudStrategy.get_all_workers()

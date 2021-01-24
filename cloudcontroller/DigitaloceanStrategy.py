"""
Concrete Strategies implement the algorithm while following the base Strategy
interface. The interface makes them interchangeable in the Context.
"""
from cloudcontroller.CloudStrategy import CloudStrategy
from utils.utility import init_logging
from digitalocean import SSHKey
from model.WorkerModel import Worker
import traceback
import digitalocean
import time 


class DigitalOceanStrategy(CloudStrategy):
    def __init__(self,config):
        try:
            self.logger = init_logging(__name__)
            self.token = config['do_key']
            self.region = config['region']
            self.droplet_size = config['worker_size']
            self.snapshot_id = config['image_id']
            self.manager = digitalocean.Manager(token=self.token)
            self.droplets = []
        except Exception as e:
            self.logger.error(
                f"__init__@DigitalOceanStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")

    def create_worker(self,worker_name=None):
        try:
            droplet_name = worker_name
            droplet = digitalocean.Droplet(token=self.token,
                                name=droplet_name,
                                region=self.region,
                                image=self.snapshot_id, 
                                size=self.droplet_size,
                                ssh_keys=self.manager.get_all_sshkeys(),
                                backups=False)
            droplet.create()
            cond = True
            while cond:
                actions = droplet.get_actions()
                for action in actions:
                    action.load()
                    if action.status == "completed":
                        cond=False
                # This sleep does prevent rate limiting when creating squads.
                time.sleep(8)
            return True
        except Exception as e:
            self.logger.error(
                f"create_worker@DigitalOceanStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
            return False

    def delete_worker(self, worker_name):
        try:
            my_droplets = self.manager.get_all_droplets()
            for droplet in my_droplets:
                if droplet.name == worker_name:
                    droplet.destroy()
                    return True
            return False 
        except Exception as e:
            self.logger.error(
                f"delete_worker@DigitalOceanStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
            return False

    def delete_all_workers(self):
        try:
            my_droplets = self.manager.get_all_droplets()
            for droplet in my_droplets:
                droplet.destroy()
            return True
        except Exception as e:
            self.logger.error(
                f"delete_all_workers@DigitalOceanStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
            return False

    def get_all_workers(self):
        try:
            my_droplets = self.manager.get_all_droplets()
            worker_list = []
            for droplet in my_droplets:
                worker = Worker(droplet.name,  droplet.size_slug, droplet.ip_address, droplet.created_at)
                worker_list.append(worker)
            return worker_list
        except Exception as e:
            self.logger.error(
                f"get_all_workers@DigitalOceanStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
            return False

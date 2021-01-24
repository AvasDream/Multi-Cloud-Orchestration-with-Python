import yaml
import random
import string
from model.WorkerModel import Worker
from cloudcontroller.CloudContext import CloudContext
from cloudcontroller.AmazonWebServicesStrategy import AmazonWebServicesStrategy
from cloudcontroller.DigitaloceanStrategy import DigitalOceanStrategy


def read_config(file_path):
    config_file = open(file_path)
    config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
    return config_dict


def main():
    aws_config = read_config("config/aws.yaml")
    do_config = read_config("config/digitalocean.yaml")
    
    digitalocean_strategy = DigitalOceanStrategy(do_config)
    print("Cloud context set to Digitalocean")
    cloud_context = CloudContext(digitalocean_strategy)
    worker_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    print(f"Create worker {worker_name} - {cloud_context.create_worker(worker_name)}")
    worker_list = cloud_context.get_all_workers()
    print(f"Worker Objects: {worker_list}")
    for worker in worker_list:
        print(f"Worker: {worker.name} | {worker.ip} | {worker.size} | {worker.created_at}")
    print(f"Delete all workers - {cloud_context.delete_all_workers()}")
    
    print("Switching context to AWS")
    aws_strategy = AmazonWebServicesStrategy(aws_config)
    cloud_context.CloudStrategy = aws_strategy
    worker_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    print(f"Create worker {worker_name} - {cloud_context.create_worker(worker_name)}")
    worker_list = cloud_context.get_all_workers()
    print(f"Worker Objects: {worker_list}")
    for worker in worker_list:
        print(f"Worker: {worker.name} | {worker.ip} | {worker.size} | {worker.created_at}")
    print(f"Delete all workers - {cloud_context.delete_all_workers()}")

if __name__ == "__main__":
    main()
"""
    Prerequisites:
    - Config file with the following structure:
        cloud: aws
        access_key: sdfgh
        secret_key: fsdghjfg
        worker_size: t2.micro
        region: eu-central-1
        image_id: ami-01a724a06f3361337
        security_group: sg-0611318194631337
        subnet_id: subnet-05390973cac11337
        ssh:
        # Set this to a not existing key_name and path and it will be created and added to your aws region
        private_key: True
        key_name: key-name
        key_path: config/ssh/key.pem
        username: ubuntu
"""
from cloudcontroller.CloudStrategy import CloudStrategy
from utils.utility import init_logging
from model.WorkerModel import Worker
import traceback
import os
import time
import boto3
from pathlib import Path

class AmazonWebServicesStrategy(CloudStrategy):
    def __init__(self,config):
        try:
            self.logger = init_logging(__name__)
            if not os.path.isfile(str(Path.home())+"/.aws/credentials"):
                self.__configure_environment(config)
            self.ec2_res = boto3.resource('ec2', region_name=config['region'])
            self.client = boto3.client('ec2', region_name=config['region'])
            self.ec2_size = config['worker_size']
            self.ami_id = config['image_id']
            self.security_group_id = config['security_group']
            self.subnet_id = config['subnet_id']
            self.key_name = config['ssh']['key_name']
        except Exception as e:
            self.logger.error(
                f"__init__@AmazonWebServicesStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
        
    def __configure_environment(self,config):
        try:
            home_path = str(Path.home())
            creds_path = home_path + "/.aws/credentials"
            if not os.path.isfile(creds_path):
                aws_folder = home_path + "/.aws"
                if not os.path.isfile(aws_folder):
                    os.makedirs(aws_folder)
                creds_file = open(creds_path,"w")
                creds_file.write(f"[default]\naws_access_key_id = {config['access_key']}\naws_secret_access_key = {config['secret_key']}\n")

        except Exception as e:
            self.logger.error(
                f"__configure_environment@AmazonWebServicesStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")

    
    def create_worker(self, worker_name=None):
        try:
            instance_params = {
                'ImageId': self.ami_id, 'InstanceType': self.ec2_size, 'KeyName': self.key_name, 
            }
            response = self.ec2_res.create_instances(**instance_params, 
                MinCount=1, 
                MaxCount=1, 
                NetworkInterfaces=[{'SubnetId': self.subnet_id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [self.security_group_id]}]
            )
            instance = response[0]
            status = instance.state['Name']
            while status == 'pending':
                time.sleep(10)
                instance.load()
                status = instance.state['Name']
            if status == 'running':
                self.ec2_res.create_tags(Resources=[instance.id], Tags=[{'Key':'name', 'Value':worker_name}])
                self.ec2_res.create_tags(Resources=[instance.id], Tags=[{'Key':'automation-test', 'Value':'42'}])
            return True
        except Exception as e:
            self.logger.error(
                f"create_worker@AmazonWebServicesStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
            return False
        

    
    def delete_worker(self, worker_name):
        try:
            filters = [
                {
                    'Name': 'instance-state-name', 
                    'Values': ['running']
                }
            ]
            response = self.ec2_res.instances.filter(Filters=filters)
            worker_list = []
            for instance in response:
                for tag in instance.tags:
                    if 'name'in tag['Key']:
                        current_worker_name = tag['Value']
                        if current_worker_name == worker_name:
                            response = instance.terminate()
                            status = instance.state['Name']
                            while status != 'terminated':
                                time.sleep(10)
                                instance.load()
                                status = instance.state['Name']
                            return True
            return False
        except Exception as e:
            self.logger.error(
                f"delete_worker@AmazonWebServicesStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
            return False

    
    def delete_all_workers(self):
        try:
            filters = [
                {
                    'Name': 'instance-state-name', 
                    'Values': ['running']
                }
            ]
            response = self.ec2_res.instances.filter(Filters=filters)
            worker_list = []
            for instance in response:
                for tag in instance.tags:
                    if 'automation-test'in tag['Key']:
                        instance.terminate()
            return True
        except Exception as e:
            self.logger.error(
                f"delete_all_workers@AmazonWebServicesStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
            return False

    
    def get_all_workers(self):
        try:
            filters = [
                {
                    'Name': 'instance-state-name', 
                    'Values': ['running']
                }
            ]
            response = self.ec2_res.instances.filter(Filters=filters)
            worker_list = []
            for instance in response:
                for tag in instance.tags:
                    if 'name'in tag['Key']:
                        worker_name = tag['Value']
                worker = Worker(worker_name,  instance.instance_type, instance.public_ip_address, instance.launch_time)
                worker_list.append(worker)
            return worker_list
        except Exception as e:
            self.logger.error(
                f"get_all_workers@AmazonWebServicesStrategy.Exception: {e}\nTraceback\n{traceback.format_exc()}\n")
            return False

    
  
from typing import Optional
from Aws.BaseClient import BaseClient
from Aws.Ec2.Region import Region
from Aws.Iterator import Iterator


class Client(BaseClient):
    """
    EC2 Client
    """
    __client_identifier__ = 'ec2'

    def __init__(self, credential, region_name):
        """
        Setup an EC2 client

        :param credential: The credential used to authenticate to AWS
        :type credential: Credential

        :param region_name: Region in which client will operate
        :type region_name: str
        """
        super().__init__(credential, region_name)

    def describe_regions(self) -> Optional[Region]:
        """
        Describe a region

        :return: Region object, or None if not found
        """
        return None

    def run_instances(
            self,
            instance_type=None,
            image_id=None,
            user_data=None,
            shutdown_behavior=None,
            network_interfaces=None,
            min_count=1,
            max_count=1
    ):
        """
        Start a new EC2 instance

        :param instance_type: Optional Ec2 Instance type/size
        :type instance_type: Optional[str]

        :param image_id: Optional Instance AMI ID to run the instance with
        :type image_id: Optional[str]

        :param shutdown_behavior: Optional behaviour of the EC2 instance storage when shutdown
        :type shutdown_behavior: Optional[str]

        :param user_data: Optional Bash script to run on the instance at startup
        :type user_data: Optional[str]

        :param network_interfaces: Optional dict for the creation of a network interface to attach to the instance
        :type network_interfaces: Optional[Dict]

        :param min_count: Optional count for minimum instances to launch
        :type min_count: Optional[int]

        :param max_count: Optional count for maximum instances to launch
        :type max_count: Optional[int]

        :return: Run instances object
        """

        return self.__client__.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            UserData=user_data,
            MinCount=min_count,
            MaxCount=max_count,
            InstanceInitiatedShutdownBehavior=shutdown_behavior,
            NetworkInterfaces=network_interfaces
        )

    def describe_instance(self, instance_ids=None):
        """
        Describe an EC2 Instance

        :param instance_ids: ARN of the task definition to describe
        :type instance_ids: str

        :return: Describe instance object
        """
        instances = Iterator.iterate(
            client=self.__client__,
            method_name='describe_instances',
            data_key='Reservations',
            arguments={
                'InstanceIds': instance_ids
            }
        )

        return instances

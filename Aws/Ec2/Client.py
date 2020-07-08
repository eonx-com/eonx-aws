from typing import Optional
from Aws.BaseClient import BaseClient
from Aws.Ec2.Region import Region
from Aws.Iterator import Iterator
from Aws.Instance import Instance



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
            image_id,
            min_count,
            max_count,
            instance_type=None,
            user_data=None,
            shutdown_behavior=None,
            network_interfaces=None,
    ):
        """
        Start a new EC2 instance

        :param image_id: Instance AMI ID to run the instance with
        :type image_id: str

        :param min_count: Count for minimum instances to launch
        :type min_count: int

        :param max_count: Count for maximum instances to launch
        :type max_count: int

        :param instance_type: Optional Ec2 Instance type/size
        :type instance_type: Optional[str]

        :param shutdown_behavior: Optional behaviour of the EC2 instance storage when shutdown
        :type shutdown_behavior: Optional[str]

        :param user_data: Optional Bash script to run on the instance at startup
        :type user_data: Optional[str]

        :param network_interfaces: Optional dict for the creation of a network interface to attach to the instance
        :type network_interfaces: Optional[Dict]

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

    def describe_instance(self, instance_ids):
        """
        Describes EC2 instances

        :param instance_ids: ID's of the EC2 Instances to describe
        :type instance_ids: list

        :return: Describe instances object
        """

        result = Iterator.iterate(
            client=self.__client__,
            method_name='describe_instances',
            data_key='Reservations',
            arguments={
                'InstanceIds': instance_ids
            }
        )

        if 'Reservations' not in result:
            raise Exception(
                'Unexpected result when describing instances ({instance_ids}), could not find expected "Reservations" key'.format(instance_ids=instance_ids))

        if len(result['Reservations']) == 0:
            return None

        instance = Instance(instance_ids)
        instance.set_values(result['Reservations'][0])

        return instance

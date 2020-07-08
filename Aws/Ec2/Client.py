from typing import Optional
from Aws.BaseClient import BaseClient
from Aws.Ec2.Region import Region


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

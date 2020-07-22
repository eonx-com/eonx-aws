from typing import Optional, Dict

from Aws.Iterator import Iterator

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

    def describe_regions(self) -> Dict[str, Region]:
        """
        Describe a region

        :return: Dictioanry of regions indexed by region name
        """
        regions = {}

        describe_regions = Iterator.iterate(
            client=self.__client__,
            method_name='describe_regions',
            data_key='Regions'
        )

        for region in describe_regions:
            regions[region["RegionName"]] = region

        return regions

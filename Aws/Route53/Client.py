from Aws.BaseClient import BaseClient
from Aws.Iterator import Iterator
from typing import Optional

from Aws.Lambda.Log import Log


class Client(BaseClient):
    """
    ECS Client
    """
    __client_identifier__ = 'route53'

    def __init__(self, credential, region_name):
        """
        Setup an ECS client

        :param credential: The credential used to authenticate to AWS
        :type credential: Credential

        :param region_name: Region in which client will operate
        :type region_name: str
        """
        super().__init__(credential, region_name)

    def list_hosted_zones_by_id(self) -> dict:
        """
        List all available hosted zones indexed by ID

        :return: Dictionary of ECS clusters indexed by their ARN
        """
        hosted_zones = {}

        hosted_zone_ids = Iterator.iterate(
            client=self.__client__,
            method_name='list_hosted_zones',
            data_key='HostedZones'
        )

        for hosted_zone in hosted_zone_ids:
            hosted_zones[hosted_zone['Id']] = hosted_zone

        return hosted_zones

    def list_hosted_zones_by_name(self) -> dict:
        """
        List all available hosted zones indexed by name

        :return: Dictionary of ECS clusters indexed by their ARN
        """
        hosted_zones = {}

        hosted_zone_ids = Iterator.iterate(
            client=self.__client__,
            method_name='list_hosted_zones',
            data_key='HostedZones'
        )

        for hosted_zone in hosted_zone_ids:
            hosted_zones[hosted_zone['Name']] = hosted_zone

        return hosted_zones

    def create_name_server_record(self, hosted_zone_name, domain_name, name_servers) -> dict:
        """
        List all available hosted zones indexed by name

        :param hosted_zone_name: Hosted zone name
        :type hosted_zone_name: str

        :param domain_name: The domain name being delegated
        :type domain_name: str

        :param name_servers: List of name servers
        :type name_servers: List[str]

        :return: Dictionary of ECS clusters indexed by their ARN
        """
        hosted_zones = self.list_hosted_zones_by_name()

        if hosted_zone_name not in hosted_zones:
            raise Exception('Could not locate requested hosted zone ({hosted_zone_name})'.format(hosted_zone_name=hosted_zone_name))

        resource_records = []
        for value in name_servers:
            resource_records.append({'Value': value})

        try:
            self.__client__.change_resource_record_sets(
                HostedZoneId = hosted_zones[hosted_zone_name]['Id'],
                ChangeBatch={
                    'Comment': 'Delegate domain to project/environment account',
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': domain_name,
                                'Type': 'NS',
                                'TTL': 60,
                                'ResourceRecords': resource_records
                            }
                        }
                    ]
                }
            )
        except Exception as e:
            raise Exception('Could not delegate domain name ({domain_name})'.format(domain_name=domain_name))
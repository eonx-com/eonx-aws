from typing import Any, Optional

from Aws.BaseClient import BaseClient
from Aws.Iterator import Iterator


class Client(BaseClient):
    """
    Logs Client
    """
    __client_identifier__ = 'logs'

    def __init__(self, credential, region_name):
        """
        Setup a Cloudwatch Logs client

        :param credential: The credential used to authenticate to AWS
        :type credential: Credential

        :param region_name: Region in which client will operate
        :type region_name: str
        """
        super().__init__(credential, region_name)

    def get_log_events(self, log_group_name, log_stream_name) -> Any:
        """
        Invoke a lambda function

        :param log_group_name: Log group name
        :type log_group_name: str

        :param log_stream_name: Log stream name
        :type log_stream_name: str

        :return: Return value
        """
        log_events = Iterator.iterate(
            client=self.__client__,
            method_name='get_log_events',
            data_key='events',
            token_key_read='nextForwardToken',
            token_key_write='nextToken',
            arguments={
                'logGroupName': log_group_name,
                'logStreamName': log_stream_name,
                'startFromHead': True
            }
        )

        return log_events


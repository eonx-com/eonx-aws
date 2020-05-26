from typing import Any, Optional

from Aws.BaseClient import BaseClient


class Client(BaseClient):
    """
    ECS Client
    """
    __client_identifier__ = 'lambda'

    def __init__(self, credential, region_name):
        """
        Setup an ECS client

        :param credential: The credential used to authenticate to AWS
        :type credential: Credential

        :param region_name: Region in which client will operate
        :type region_name: str
        """
        super().__init__(credential, region_name)

    def invoke(self, function_name, payload) -> Any:
        """
        Invoke a lambda function

        :param function_name: Name of the function
        :type function_name: str

        :param payload: JSON payload
        :type payload: str

        :return: Return value
        """
        result = self.__client__.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=payload or '{}'
        )

        return result


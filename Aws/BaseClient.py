from Aws.Credential import Credential
from Aws.Lambda.Log import Log


class BaseClient:
    """
    ECS Client
    """
    __session__ = None
    __client__ = None
    __client_identifier__ = None

    def __init__(self, credential, region_name):
        """
        Setup an AWS client

        :param credential: The credential used to authenticate to AWS
        :type credential: Credential

        :param region_name: Region in which client will operate
        :type region_name: str
        """
        if self.__client_identifier__ is None:
            raise Exception('Attempting to retrieve client but no identifier has been set')

        # If no credential is supplied- use default system permission
        if credential is None:
            Log.trace('Using default system credentials')
            credential = Credential()

        self.__credential__ = credential
        self.__session__ = credential.get_boto3_session(region_name)
        self.__client__ = self.__session__.client(self.__client_identifier__)

from Aws.Credential import Credential
from Aws.Lambda.Log import Log


class BaseClient:
    """
    ECS Client
    """
    __session__ = None
    __client__ = None
    __client_identifier__ = None
    __caller_identity__ = None

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

        self.__sts_client__ = self.__session__.client("sts")
        self.__caller_identity__ = self.__sts_client__.get_caller_identity()

    def get_caller_user_id(self) -> str:
        """
        Get the AWS user ID
        """
        return self.__caller_identity__['UserId']

    def get_caller_aws_account_id(self) -> str:
        """
        Get the AWS account ID
        """
        return self.__caller_identity__['Account']

    def get_caller_arn(self) -> str:
        """
        Get the AWS user ARN
        """
        return self.__caller_identity__['Arn']

from typing import Optional

import boto3
import hashlib

from boto3 import Session


class Credential:
    """
    AWS credentials object
    """
    __cache__ = {}
    __profile_name__ = None
    __aws_access_key_id__ = None
    __aws_secret_access_key__ = None
    __aws_session_token__ = None
    __iam_role_arn__ = None

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, iam_role_arn=None, profile_name=None):
        """
        Initialize credentials object

        :param aws_access_key_id: AWS access key ID value
        :type aws_access_key_id: Optional[str]
        :param aws_secret_access_key: AWS secret access key value
        :type aws_secret_access_key: Optional[str]
        :param aws_session_token: AWS session token value
        :type aws_session_token: Optional[str]
        """
        self.__cache__ = {}
        self.set_aws_access_key_id(aws_access_key_id)
        self.set_aws_secret_access_key(aws_secret_access_key)
        self.set_aws_session_token(aws_session_token)
        self.set_iam_role_arn(iam_role_arn)
        self.set_profile_name(profile_name)

    def get_boto3_session(self, region_name, cache=True) -> Session:
        """
        Use these credentials to return a Boto3 session object

        :param region_name: The AWS region for the session to be created in
        :type region_name: str

        :param cache: Flag indicating the credential should be cached for future get_boto3_session() calls
        :type cache: bool

        :return: Boto3 Session object
        
        :raise Exception: on authentication failure
        """
        session_name = str(self.__aws_access_key_id__) or ''
        session_name = session_name + str(self.__aws_secret_access_key__) or ''
        session_name = session_name + str(self.__aws_session_token__) or ''
        session_name = session_name + str(self.__profile_name__) or ''
        session_name = session_name + str(region_name)
        session_name = hashlib.md5(session_name.encode())
        session_name = str(session_name.hexdigest())

        # If we are caching, return cached copy
        if cache is True and session_name in self.__cache__.keys():
            return self.__cache__[session_name]

        session = boto3.session.Session(
            aws_access_key_id=self.__aws_access_key_id__,
            aws_secret_access_key=self.__aws_secret_access_key__,
            aws_session_token=self.__aws_session_token__,
            region_name=region_name,
            profile_name=self.__profile_name__
        )

        # If we are caching, persist this session to the cache
        if cache is True:
            self.__cache__[session_name] = session

        return session

    def get_profile_name(self) -> Optional[str]:
        """
        Retrieve AWS profile name
        :return: AWS profile name or None if not set
        """
        return self.__profile_name__

    def set_profile_name(self, profile_name) -> None:
        """
        Set AWS profile name

        :param profile_name: AWS profile name
        :type profile_name: Optional[str]
        """
        self.__profile_name__ = profile_name

    def get_iam_role_arn(self) -> Optional[str]:
        """
        Retrieve AWS IAM role ARN
        :return: AWS IAM role ARN or None if not set
        """
        return self.__iam_role_arn__

    def set_iam_role_arn(self, iam_role_arn) -> None:
        """
        Set AWS IAM role ARN

        :param iam_role_arn: AWS IAM role ARN
        :type iam_role_arn: Optional[str]
        """
        self.__iam_role_arn__ = iam_role_arn

    def get_aws_access_key_id(self) -> Optional[str]:
        """
        Retrieve AWS access key ID
        :return: AWS access key ID or None if not set
        """
        return self.__aws_access_key_id__

    def set_aws_access_key_id(self, aws_access_key_id) -> None:
        """
        Set AWS access key ID

        :param aws_access_key_id: AWS access key ID value
        :type aws_access_key_id: Optional[str]
        """
        self.__aws_access_key_id__ = aws_access_key_id

    def get_aws_secret_access_key(self) -> Optional[str]:
        """
        Retrieve AWS access key secret
        :return: AWS access key secret or None if not set
        """
        return self.__aws_secret_access_key__

    def set_aws_secret_access_key(self, aws_secret_access_key) -> None:
        """
        Set AWS access key secret

        :param aws_secret_access_key: AWS secret access key value
        :type aws_secret_access_key: Optional[str]
        """
        self.__aws_secret_access_key__ = aws_secret_access_key

    def get_aws_session_token(self) -> Optional[str]:
        """
        Retrieve AWS session token (if any)
        :return: AWS session token, or None if not set
        """
        return self.__aws_session_token__

    def set_aws_session_token(self, aws_session_token) -> None:
        """
        Set AWS session token

        :param aws_session_token: AWS session token value
        :type aws_session_token: Optional[str]
        """
        self.__aws_session_token__ = aws_session_token

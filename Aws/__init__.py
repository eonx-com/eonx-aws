import boto3
import hashlib

from boto3 import Session


class Iam:
    @staticmethod
    def assume_iam_role(role_arn) -> dict:
        """
        :param role_arn: The IAM role to impersonate
        :type role_arn: str

        :return: Dictionary containing credentials

        :raise Exception: on failure to assume role
        """

        session_name = hashlib.md5(role_arn.encode())

        sts_client = boto3.client('sts')
        assume_role_response = sts_client.assume_role(RoleArn=role_arn, RoleSessionName=session_name)

        if 'Credentials' in assume_role_response:
            return assume_role_response['Credentials']

        raise Exception('Failed to assume IAM role ({role_arn})'.format(role_arn=role_arn))

    @staticmethod
    def authenticate(aws_access_key_id, aws_secret_access_key, region_name, profile_name='sts', aws_session_token=None) -> Session:
        """
        Start AWS session using supplied credentials

        :param aws_access_key_id: The AWS access key ID
        :type aws_access_key_id: str

        :param aws_secret_access_key: The AWS access key secret
        :type aws_secret_access_key: str

        :param region_name: The region in which we want to authenticate
        :type region_name: str

        :param profile_name: Optional AWS session profile name (defaults to 'sts')
        :type profile_name: str

        :param aws_session_token: Optional AWS access key session token
        :type aws_session_token: str

        :return: Boto3 session
        """
        return boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            profile_name=profile_name
        )

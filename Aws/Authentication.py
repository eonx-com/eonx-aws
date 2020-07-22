import boto3
import hashlib

from Aws.Credential import Credential


class Authentication:
    @staticmethod
    def get_credential_for_profile_name(profile_name) -> Credential:
        """
        Use AWS profile name to get credential object

        :param profile_name: AWS profile name
        :type profile_name: str

        :return: AWS credentials object
        """
        return Credential(
            profile_name=profile_name
        )

    @staticmethod
    def get_credential_for_key_secret(aws_access_key_id, aws_secret_access_key, aws_session_token=None) -> Credential:
        """
        Use AWS key/secret to get credential object

        :param aws_access_key_id: The AWS access key ID
        :type aws_access_key_id: str

        :param aws_secret_access_key: The AWS access key secret
        :type aws_secret_access_key: str

        :param aws_session_token: Optional AWS session token
        :type aws_session_token: Optional[str]

        :return: AWS credentials object
        """
        return Credential(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )

    @staticmethod
    def get_credential_default() -> Credential:
        return Credential()

    @staticmethod
    def get_credential_for_iam_role(role_arn) -> Credential:
        """
        Assume an IAM role and return credential object

        :param role_arn: The IAM role to impersonate
        :type role_arn: str

        :return: AWS credentials object

        :raise Exception: on failure to assume role
        """
        session_name = hashlib.md5(role_arn.encode())
        session_name = str(session_name.hexdigest())

        sts_client = boto3.client('sts')
        assume_role_response = sts_client.assume_role(RoleArn=role_arn, RoleSessionName=session_name)

        if 'Credentials' in assume_role_response:
            return Credential(
                aws_access_key_id=assume_role_response['Credentials']['AccessKeyId'],
                aws_secret_access_key=assume_role_response['Credentials']['SecretAccessKey'],
                aws_session_token=assume_role_response['Credentials']['SessionToken']
            )

        raise Exception('Failed to assume IAM role ({role_arn})'.format(role_arn=role_arn))

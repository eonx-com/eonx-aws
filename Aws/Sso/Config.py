import boto3
import json
import os

from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from Aws.Sso.ConfigException import ConfigException


class Config:
    """
    This class is a kludge to workaround the incompatibility between the v2 AWS CLI SSO login implementation and Boto3 named profiles. It will read the
    STS credentials from the ~/.aws/sso/cache folder and update the ~/.aws/credentials file the the appropriate named profile
    """
    __aws_config_path__ = f'{Path.home()}/.aws/config'
    __aws_credential_path__ = f'{Path.home()}/.aws/credentials'
    __aws_sso_cache_path__ = f'{Path.home()}/.aws/sso/cache'
    __aws_default_region__ = 'ap-southeast-2'

    @staticmethod
    def set_profile_credentials(profile_name) -> None:
        """
        Update AWS configuration with credentials for the specified SSO profile

        :param profile_name: The AWS profile name
        :type profile_name: str

        :raises ConfigException: on error during profile setup
        """
        profile = Config.__get_aws_profile__(profile_name)
        cached_login = Config.__get_sso_cached_login__(profile)
        credentials = Config.__get_sso_role_credentials__(profile, cached_login)
        Config.__update_aws_credentials__(profile_name, profile, credentials)

    @staticmethod
    def __get_sso_cached_login__(profile) -> dict:
        """
        Get SSO cached login details for profile

        :param profile: The configuration profile
        :type profile: dict

        :raises ConfigException: if SSO credentials have expired or are invalid
        """
        file_paths = Config.__list_directory__(Config.__aws_sso_cache_path__)

        for file_path in file_paths:
            data = Config.__load_json__(file_path)

            if data.get('startUrl') != profile['sso_start_url']:
                continue

            if data.get('region') != profile['sso_region']:
                continue

            found = True

            # Make sure it hasn't expired
            if datetime.utcnow() > Config.__parse_timestamp__(data['expiresAt']):
                continue

            # Return the cached login details
            return data

        if found is True:
            raise ConfigException('The requested SSO login profile has an expired token')

        raise ConfigException('The requested SSO login profile was not found')

    @staticmethod
    def __get_sso_role_credentials__(profile, login) -> dict:
        """
        Return SSO credentials for profile

        :param profile:
        :type profile: dict

        :param login:
        :type login: dict

        :return: dict
        """
        client = boto3.client('sso', region_name=profile['sso_region'])
        response = client.get_role_credentials(
            roleName=profile['sso_role_name'],
            accountId=profile['sso_account_id'],
            accessToken=login['accessToken'],
        )
        return response['roleCredentials']

    @staticmethod
    def __get_aws_profile__(profile_name) -> dict:
        """
        Retrieve AWS profile from config

        :param profile_name: The profile name to retrieve
        :type profile_name: str

        :return: The profiles configuration in a dictionary
        """
        config = Config.__read_config__(Config.__aws_config_path__)
        profile_opts = config.items(f'profile {profile_name}')

        return dict(profile_opts)

    @staticmethod
    def __update_aws_credentials__(profile_name, profile, credentials) -> None:
        """
        Update AWS credentials in config

        :param profile_name: Profile name
        :type profile_name: str

        :param profile: Profile configuration
        :type profile: dict

        :param credentials: Credentials dictionary
        :type credentials: dict
        """
        region = profile.get('region', Config.__aws_default_region__)
        config = Config.__read_config__(Config.__aws_credential_path__)
        if config.has_section(profile_name):
            config.remove_section(profile_name)
        config.add_section(profile_name)
        config.set(profile_name, 'region', region)
        config.set(profile_name, 'aws_access_key_id', credentials['accessKeyId'])
        config.set(profile_name, 'aws_secret_access_key ', credentials['secretAccessKey'])
        config.set(profile_name, 'aws_session_token', credentials['sessionToken'])
        Config.__write_config__(Config.__aws_credential_path__, config)

    @staticmethod
    def __list_directory__(path) -> List[str]:
        """
        List all files in directory

        :param path: Path to list
        :type path: str

        :return: List of files in specified path
        """
        file_paths = []

        if os.path.exists(path):
            file_paths = Path(path).iterdir()

        # Sort files by most recently updated
        file_paths = sorted(file_paths, key=os.path.getmtime)
        file_paths.reverse()

        return [str(f) for f in file_paths]

    @staticmethod
    def __load_json__(path) -> Optional[dict]:
        """
        Load JSON file, ignoring invalid JSON
        :param path: File to load
        :type path: str

        :return: JSON dictionary object, or None if loading failed
        """
        try:
            with open(path) as context:
                return json.load(context)
        except ValueError:
            # Ignore invalid json
            return None

    @staticmethod
    def __parse_timestamp__(value) -> datetime:
        """
        Parse string timestamp to datetime object

        :param value: String timestamp
        :type value: str

        :return: Datetime object
        """
        # noinspection SpellCheckingInspection
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SUTC')

    @staticmethod
    def __read_config__(path) -> ConfigParser:
        """
        Read config file

        :param path: Configuration filename
        :type path: str

        :return: Configuration parser
        """
        config = ConfigParser()
        config.read(path)
        return config

    @staticmethod
    def __write_config__(path, config) -> None:
        """
        Write configuration file

        :param path: Configuration filename
        :type path: str

        :param config: Configuration to write
        :type config: ConfigParser
        """
        with open(path, 'w') as destination:
            config.write(destination)

import os
import unittest
import warnings
from pprint import pprint
from time import time, sleep

import botocore

from Aws.Credential import Credential
from Aws.Ec2.Client import Client


class TestEc2Client(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup for unit tests
        """
        # Store timestamp for use in identifying resources created by tests
        self.timestamp = int(time())

        # Boto3 leaves a socket connection unclosed, this disables the following warning that is received during unit tests
        # ResourceWarning: unclosed <ssl.SSLSocket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('192.168.1.84', 41910), raddr=('52.46.134.192', 443)>
        print('Disabling unclosed socket warning')
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

        # Retrieve AWS credentials from CLI
        print('Retrieving AWS credentials')
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        # If either variable is not set the tests cannot proceed
        if aws_access_key_id is None or aws_secret_access_key is None:
            raise Exception("AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY credentials must be set in environment variables prior to running unit tests")

        # Setup QLDB client
        print('Creating EC2 client')
        credential = Credential(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.client = Client(credential=credential, region_name='ap-southeast-2')

    def test_describe_regions(self):
        """
        Test describe regions
        """
        print('Describing regions')
        regions = self.client.describe_regions()

        print('Validating response contains expected values')
        if 'ap-southeast-2' not in regions.keys():
            raise Exception('Could not locate expected region in response')
        if 'Endpoint' not in regions['ap-southeast-2'].keys():
            raise Exception('Could not locate expected Endpoint key in response')
        if 'OptInStatus' not in regions['ap-southeast-2'].keys():
            raise Exception('Could not locate expected OptInStatus key in response')
        if 'RegionName' not in regions['ap-southeast-2'].keys():
            raise Exception('Could not locate expected RegionName key in response')


import os
import unittest
import warnings
from time import time, sleep

import botocore

from Aws.Credential import Credential
from Aws.Qldb.Client import Client
from Aws.Qldb.LedgerState import LedgerState


class TestQldbClient(unittest.TestCase):
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
        print('Creating QLDB client')
        credential = Credential(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.client = Client(credential=credential, region_name='ap-southeast-2')

    def test_create_delete_ledger(self):
        """
        Test creation/deletion of ledger
        """
        name = "UnitTest{timestamp}".format(timestamp=self.timestamp)
        print('Creating QLDB ledger ({name})'.format(name=name))
        self.client.create_ledger(
            name=name,
            tags={'Description': 'This ledger was created by Python unit tests and can be deleted'},
            deletion_protection=True
        )

        print('Waiting for ledger to become active')
        while True:
            sleep(3)
            ledger = self.client.describe_ledger(name=name)
            state = ledger.get('State')
            if state != LedgerState.CREATING.value:
                break

        if state != LedgerState.ACTIVE.value:
            raise Exception('Unexpected ledger status ({state}), expected ACTIVE'.format(state=state))

        print('Deleting QLDB ledger ({name})'.format(name=name))
        self.client.delete_ledger(name=name, force=True)

        print('Checking ledger status is DELETING')
        ledger = self.client.describe_ledger(name=name)
        state = ledger.get('State')
        if state != LedgerState.DELETING.value:
            raise Exception('Unexpected ledger status ({state}), expected DELETING'.format(state=state))

        # Attempt to describe the ledger until we hit a ResourceNotFoundException. If this doesn't happen within 2 minutes, assume deletion failed
        print('Waiting for ledger deletion to complete')
        count = 0
        while True:
            sleep(6)
            try:
                ledger = self.client.describe_ledger(name=name)
                if state != LedgerState.DELETING.value:
                    raise Exception('Unexpected ledger status ({state}), expected DELETING'.format(state=state))
            except botocore.errorfactory.ResourceNotFoundException:
                return

            # After 20 attempts, give up waiting for deletion
            count = count + 1
            if count == 20:
                break

        raise Exception('Timed out waiting for deletion of QLDB ledger')

    def test_list_ledgers(self):
        """
        Test list ledgers returns the expected result
        """
        print('Listing ledgers')
        ledgers = self.client.list_ledgers()

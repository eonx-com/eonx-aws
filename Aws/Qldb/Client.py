from typing import Optional, Dict

from Aws.Credential import Credential

from Aws.BaseClient import BaseClient
from Aws.Iterator import Iterator
from Aws.Qldb.Ledger import Ledger


class Client(BaseClient):
    """
    Quantum Ledger Database Client
    """
    __client_identifier__ = 'qldb'

    def __init__(self, credential: Credential, region_name: str):
        """
        Setup a QLDB client

        :param credential: The credential used to authenticate to AWS
        :param region_name: Region in which client will operate
        """
        super().__init__(credential, region_name)

    def create_ledger(
            self,
            name,
            tags: Optional[Dict[str, str]] = None,
            deletion_protection: bool = False
    ) -> Ledger:
        """
        Create a new ledger

        :return: Ledger object
        """
        response = self.__client__.create_ledger(
            Name=name,
            Tags=tags,
            PermissionsMode='ALLOW_ALL',
            DeletionProtection=deletion_protection
        )

        ledger = Ledger(response['Arn'])
        ledger.set_values(response)
        return ledger

    def delete_ledger(self, name: str, force: bool = False) -> None:
        """
        Delete QLDB ledger

        :param name: Name of the ledger to delete
        :param force: Boolean flag, if True will disable deletion protection
        """
        if force is True:
            self.__client__.update_ledger(
                Name=name,
                DeletionProtection=False
            )

        self.__client__.delete_ledger(Name=name)

    def describe_ledger(self, name: str) -> Ledger:
        """
        Describe QLDB ledger

        :param name: Name of the ledger to describe
        :return: Ledger object
        """
        describe_ledger_response = self.__client__.describe_ledger(Name=name)
        ledger = Ledger(describe_ledger_response['Name'])
        ledger.set_values(describe_ledger_response)

        return ledger

    def list_ledgers(self) -> Dict[str, Ledger]:
        """
        List QLDB ledgers

        :return: Dictionary of ledger objects indexed by their ARN
        """
        ledgers = {}

        ledger_names = Iterator.iterate(
            client=self.__client__,
            method_name='list_ledgers',
            data_key='Ledgers'
        )

        for ledger_name in ledger_names:
            ledger = self.describe_ledger(ledger_name['Name'])
            ledgers[ledger.get('Arn')] = ledger

        return ledgers

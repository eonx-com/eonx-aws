from copy import copy, deepcopy
from typing import Optional, Any


class BaseObject:
    """
    Base AWS object used to represent anything with an ARN, this should not be used directly in application code
    """
    # Object ARN
    __arn__ = None

    # Object data
    __data__ = {}

    def __init__(self, arn=None):
        """
        Initialize service object

        :param arn: The ECS services ARN
        :type arn: Optional[str]
        """
        self.set_arn(arn)

    def set(self, key, value) -> None:
        """
        Set data attribute

        :param key: The key name
        :type key: str

        :param value: The value to set
        :type value: Any
        """
        self.set(key, deepcopy(value))

    def set_values(self, values, erase=True) -> None:
        """
        Overwrite all values with those from the supplied dictionary

        :param values: The dictionary to use
        :type values: dict

        :param erase: If true, all existing values will be erased
        :type erase: bit
        """
        if erase is True:
            self.__data__ = {}

        self.__data__.update(deepcopy(values))

    def get(self, key) -> Any:
        """
        Get data attribute

        :param key: The key name
        :type key: str

        :param value: The value to set
        :type value: Any

        :return: The specified value, or None if it is not set
        """
        if key not in self.__data__.keys():
            return None

        return self.__data__[key]

    def to_dict(self) -> dict:
        """
        Return all data as a dictionary

        :return: Dictionary of data
        """
        return self.__data__

    def set_arn(self, arn):
        """
        Set the services ARN

        :param arn: The ECS services ARN
        :type arn: str

        :return:
        """
        self.__arn__ = arn

    def get_arn(self) -> Optional[str]:
        """
        Return the ARN of this service

        :return: The services ARN
        """
        return self.__arn__

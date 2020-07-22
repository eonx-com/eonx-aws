from Aws.BaseObject import BaseObject


class Ledger(BaseObject):
    """
    Ledger
    """

    def __init__(self, arn):
        """
        Initialize ledger object

        :param arn: The ledger ARN
        :type arn: str
        """
        # Call parent object init function
        super().__init__(arn)

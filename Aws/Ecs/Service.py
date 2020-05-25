from Aws.BaseObject import BaseObject


class Service(BaseObject):
    """
    ECS Service
    """
    def __init__(self, arn):
        """
        Initialize service object

        :param arn: The ECS services ARN
        :type arn: str
        """
        # Call parent object init function
        super().__init__(arn)

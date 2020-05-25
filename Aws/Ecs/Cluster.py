from Aws.BaseObject import BaseObject


class Cluster(BaseObject):
    """
    ECS Cluster
    """
    def __init__(self, arn):
        """
        Initialize service object

        :param arn: The ECS services ARN
        :type arn: str
        """
        # Call parent object init function
        super().__init__(arn)

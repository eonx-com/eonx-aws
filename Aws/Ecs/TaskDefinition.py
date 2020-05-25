from Aws.BaseObject import BaseObject


class TaskDefinition(BaseObject):
    """
    ECS Task Definition
    """
    def __init__(self, arn):
        """
        Initialize task definition object

        :param arn: The ECS task definitions ARN
        :type arn: str
        """
        # Call parent object init function
        super().__init__(arn)

from Aws.BaseObject import BaseObject


class Task(BaseObject):
    """
    ECS Task
    """
    def __init__(self, arn):
        """
        Initialize task object

        :param arn: The ECS tasks ARN
        :type arn: str
        """
        # Call parent object init function
        super().__init__(arn)

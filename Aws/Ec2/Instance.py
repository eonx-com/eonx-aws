from Aws.BaseObject import BaseObject


class Instance(BaseObject):
    """
    EC2 Region
    """
    def __init__(self, instance_ids):
        """
        Initialize instance object

        :param instance_ids: The ID's of the Ec2 instances
        :type instance_ids: list
        """
        # Call parent object init function
        super().__init__(instance_ids)

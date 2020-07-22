from Aws.BaseClient import BaseClient


class Client(BaseClient):
    """
    Cloudwatch Client
    """
    __client_identifier__ = 'cloudwatch'

    # Allowed metrics
    UNIT_SECONDS = 'Seconds'
    UNIT_MICROSECONDS = 'Microseconds'
    UNIT_MILLISECONDS = 'Milliseconds'
    UNIT_BYTES = 'Bytes'
    UNIT_KILOBYTES = 'Kilobytes'
    UNIT_MEGABYTES = 'Megabytes'
    UNIT_GIGABYTES = 'Gigabytes'
    UNIT_TERABYTES = 'Terabytes'
    UNIT_BITS = 'Bits'
    UNIT_KILOBITS = 'Kilobits'
    UNIT_MEGABITS = 'Megabits'
    UNIT_GIGABITS = 'Gigabits'
    UNIT_TERABITS = 'Terabits'
    UNIT_PERCENT = 'Percent'
    UNIT_COUNT = 'Count'
    UNIT_BYTES_PER_SECOND = 'Bytes / Second'
    UNIT_KILOBYTES_PER_SECOND = 'Kilobytes / Second'
    UNIT_MEGABYTES_PER_SECOND = 'Megabytes / Second'
    UNIT_GIGABYTES_PER_SECOND = 'Gigabytes / Second'
    UNIT_TERABYTES_PER_SECOND = 'Terabytes / Second'
    UNIT_BITS_PER_SECOND = 'Bits / Second'
    UNIT_KILOBITS_PER_SECOND = 'Kilobits / Second'
    UNIT_MEGABITS_PER_SECOND = 'Megabits / Second'
    UNIT_GIGABITS_PER_SECOND = 'Gigabits / Second'
    UNIT_TERABITS_PER_SECOND = 'Terabits / Second'
    UNIT_COUNT_PER_SECOND = 'Count / Second'

    def __init__(self, credential, region_name):
        """
        Setup a Cloudwatch client

        :param credential: The credential used to authenticate to AWS
        :type credential: Credential

        :param region_name: Region in which client will operate
        :type region_name: str
        """
        super().__init__(credential, region_name)

    def put_metric(self, namespace, metric_name, value, unit):
        """
        Push a Cloudwatch metric

        :type namespace: The Cloudwatch namespace
        :param namespace: str

        :type metric_name: str
        :param metric_name: Metric name

        :type value: float
        :param value: Value to save

        :type unit: str
        :param unit: Unit of measurement (e.g. Bytes, Count)

        :return: None
        """
        self.__client__.put_metric_data(
            Namespace=namespace,
            MetricData=[{
                'MetricName': metric_name,
                'Unit': unit,
                'Value': value
            }]
        )

    def increment_count(self, namespace, metric_name):
        """
        Increment a count Cloudwatch metric

        :type namespace: The Cloudwatch namespace
        :param namespace: str

        :type metric_name: str
        :param metric_name: Metric name

        :return: None
        """
        self.__client__.put_metric_data(
            Namespace=namespace,
            MetricData=[{
                'MetricName': metric_name,
                'Unit': Client.UNIT_COUNT,
                'Value': 1.0
            }]
        )

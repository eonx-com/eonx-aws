from Aws.BaseClient import BaseClient
from Aws.Ecs.Cluster import Cluster
from Aws.Ecs.EcsException import EcsException
from Aws.Ecs.Service import Service
from Aws.Ecs.Task import Task
from Aws.Ecs.TaskDefinition import TaskDefinition
from Aws.Iterator import Iterator
from typing import Optional

from Aws.Lambda.Log import Log


class Client(BaseClient):
    """
    ECS Client
    """
    __client_identifier__ = 'ecs'

    def __init__(self, credential, region_name):
        """
        Setup an ECS client

        :param credential: The credential used to authenticate to AWS
        :type credential: Credential

        :param region_name: Region in which client will operate
        :type region_name: str
        """
        super().__init__(credential, region_name)

    def list_clusters(self) -> dict:
        """
        List all ECS clusters available

        :return: Dictionary of ECS clusters indexed by their ARN
        """
        clusters = {}

        cluster_arns = Iterator.iterate(
            client=self.__client__,
            method_name='list_clusters',
            data_key='clusterArns'
        )

        for cluster_arn in cluster_arns:
            cluster = self.describe_cluster(cluster_arn)

            if cluster is not None:
                clusters[cluster_arn] = cluster

        return clusters

    def describe_cluster(self, arn) -> Optional[Cluster]:
        """
        Describe a cluster

        :param arn: The clusters ARN
        :type arn: str

        :return: Cluster object, or None if not found
        """
        result = self.__client__.describe_clusters(
            clusters=[arn],
            include=['ATTACHMENTS', 'SETTINGS', 'STATISTICS', 'TAGS']
        )

        if 'clusters' not in result:
            raise Exception('Unexpected result when describing cluster ({arn}), could not find expected "clusters" key'.format(arn=arn))

        if len(result['clusters']) > 1:
            raise Exception('Unexpected result when describing cluster ({arn}), more than one result returned'.format(arn=arn))

        if len(result['clusters']) == 0:
            return None

        cluster = Cluster(arn)
        cluster.set_values(result['clusters'][0])

        return cluster

    def list_services(self, cluster_arn) -> dict:
        """
        List all ECS services available

        :param cluster_arn: The ARN of ECS cluster whose service you want to list
        :type cluster_arn: str

        :return: Dictionary of ECS services indexed by their ARN
        """
        services = {}

        service_arns = Iterator.iterate(
            client=self.__client__,
            method_name='list_services',
            data_key='serviceArns',
            arguments={
                'cluster': cluster_arn
            }
        )

        for service_arn in service_arns:
            service = self.describe_service(
                cluster_arn=cluster_arn,
                service_arn=service_arn
            )

            if service is not None:
                services[service_arn] = service

        return services

    def describe_service(self, cluster_arn, service_arn) -> Optional[Service]:
        """
        Describe a service
        :param cluster_arn: ARN of the cluster that hosts the service
        :type cluster_arn: str

        :param service_arn: ARN of the service to describe
        :type service_arn: str

        :return: Service object, or None if not found
        """
        result = self.__client__.describe_services(
            cluster=cluster_arn,
            services=[service_arn],
            include=['TAGS']
        )

        if 'services' not in result:
            raise Exception('Unexpected result when describing service ({arn}), could not find expected "services" key'.format(arn=service_arn))

        if len(result['services']) > 1:
            raise Exception('Unexpected result when describing service ({arn}), more than one result returned'.format(arn=service_arn))

        if len(result['services']) == 0:
            return None

        service = Service(service_arn)
        service.set_values(result['services'][0])

        return service

    def list_tasks(self, cluster_arn) -> dict:
        """
        List all ECS tasks available in the specified cluster

        :param cluster_arn: ARN of the cluster
        :type cluster_arn: str

        :return: Dictionary of ECS tasks indexed by their ARN
        """
        tasks = {}

        task_arns = Iterator.iterate(
            client=self.__client__,
            method_name='list_tasks',
            data_key='taskArns',
            arguments={
                'cluster': cluster_arn
            }
        )

        for task_arn in task_arns:
            task = self.describe_task(
                cluster_arn=cluster_arn,
                task_arn=task_arn
            )

            if task is not None:
                tasks[task_arn] = task

        return tasks

    def describe_task(self, cluster_arn, task_arn) -> Optional[Task]:
        """
        Describe a task

        :param cluster_arn: ARN of the cluster that hosts the task
        :type cluster_arn: str

        :param task_arn: ARN of the task to describe
        :type task_arn: str

        :return: Task object, or None if not found
        """
        result = self.__client__.describe_tasks(
            cluster=cluster_arn,
            tasks=[task_arn],
            include=['TAGS']
        )

        if 'tasks' not in result:
            raise Exception('Unexpected result when describing task ({arn}), could not find expected "tasks" key'.format(arn=task_arn))

        if len(result['tasks']) > 1:
            raise Exception('Unexpected result when describing task ({arn}), more than one result returned'.format(arn=task_arn))

        if len(result['tasks']) == 0:
            return None

        task = Task(task_arn)
        task.set_values(result['tasks'][0])

        return task

    def list_task_definitions(self, active=True, all_versions=False) -> dict:
        """
        List all available task definitions

        :param active: If TRUE will only return ACTIVE task definitions, if FALSE will only return INACTIVE task defintions
        :type active: bool

        :param all_versions: If TRUE all versions of the task definition will be returned, otherwise only the most recent revision will be returned
        :type all_versions: bool

        :return: Dictionary of task definitions indexed by their ARN, or None if none found
        """
        status = ('INACTIVE', 'ACTIVE')[active]

        Log.trace('Starting iteration of {status} ECS task definitions...'.format(status=status))
        task_definition_arns = Iterator.iterate(
            client=self.__client__,
            method_name='list_task_definitions',
            data_key='taskDefinitionArns',
            arguments={
                'status': status,
                'sort': 'DESC'
            }
        )

        # Prune to only most recent version
        if all_versions is False:
            Log.trace('Pruning task definition list to include most recent versions only...')
            highest_versions = {}

            for task_definition_arn in task_definition_arns:
                task_definition_arn_split = str(task_definition_arn).split(':')
                split_count = len(task_definition_arn_split)

                task_definition_version = int(task_definition_arn_split[split_count - 1])
                task_definition_identifier = task_definition_arn_split[split_count - 2]

                # If we've already seen this task definition, check if it is the highest version
                if task_definition_identifier in highest_versions.keys():
                    if highest_versions[task_definition_identifier]['version'] > task_definition_version:
                        # Already found a more recent version- skip this one
                        continue

                # Update the highest version number for this task definition
                highest_versions[task_definition_identifier] = {
                    'version': int(task_definition_version),
                    'arn': task_definition_arn
                }

            task_definition_arns.clear()

            for task_definition_identifier, highest_version in highest_versions.items():
                task_definition_arns.append(highest_version['arn'])

        task_definitions = {}

        for task_definition_arn in task_definition_arns:
            Log.trace('Describing ECS task definition: {task_definition_arn}'.format(task_definition_arn=task_definition_arn))
            task_definition = self.describe_task_definition(task_definition_arn=task_definition_arn)
            task_definitions[task_definition_arn] = task_definition

        # Prune to return only the latest version
        return task_definitions

    def describe_task_definition(self, task_definition_arn) -> TaskDefinition:
        """
        Describe a task definition

        :param task_definition_arn: ARN of the task definition to describe
        :type task_definition_arn: str

        :return: Task definition object
        """
        result = self.__client__.describe_task_definition(
            taskDefinition=task_definition_arn,
            include=['TAGS']
        )

        if 'taskDefinition' not in result:
            raise Exception('Unexpected result when describing task definition ({arn}), '
                            'could not find expected "taskDefinition" key'.format(arn=task_definition_arn))

        task_definition = TaskDefinition(task_definition_arn)
        task_definition.set_values(result['taskDefinition'])

        return task_definition

    def run_task(
            self,
            task_definition,
            cluster,
            launch_type,
            overrides=None,
            subnet_ids=None,
            security_group_ids=None,
            assign_public_ip=False,
            count=1
    ):
        """
        Start a new ECS task using the specific task definition

        :param task_definition: The task definition to be executed
        :type task_definition: TaskDefinition

        :param cluster: The ECS cluster in which the task should be started
        :type cluster: Cluster

        :param launch_type: The ECS launch type (FARGATE/EC2)
        :type launch_type: str

        :param overrides: Dictionary containing container overrides (if any)
        :type overrides: Optional[dict]

        :param subnet_ids: Optional list of subnet IDs (required for task definitions that use 'awsvpc' network mode)
        :type subnet_ids: Optional[List]

        :param security_group_ids: Optional list of security group IDs (required for task definitions that use 'awsvpc' network mode)
        :type security_group_ids: Optional[List]

        :param assign_public_ip: Optional flag indicating the task should receive a public IP address (required for task definitions that use 'awsvpc' network mode)
        :type assign_public_ip: Optional[bool]

        :param count: The number of tasks to run (defaults to 1)
        :type count: int
        """
        if launch_type not in ('FARGATE', 'EC2'):
            raise EcsException('Unknown ECS launch type requested ({launch_type}), value must be one of "FARGATE" or "EC2"'.format(launch_type=launch_type))

        # Fargate tasks must specify platform version
        platform_version = (None, 'LATEST')[launch_type == 'FARGATE']

        # If the task definition is of type 'awsvpc' then we must have valid lists of subnet IDs and security group IDs
        network_configuration = None

        if task_definition.get('networkMode') == 'awsvpc':
            if isinstance(subnet_ids, list) is False or \
               isinstance(security_group_ids, list) is False or \
               isinstance(assign_public_ip, bool) is False or \
               len(subnet_ids) == 0 or \
               len(security_group_ids) == 0:
                raise EcsException('The supplied task definition specified a network configuration of "awsvpc", valid lists are required for both the '
                                   '"subnet_ids" and "security_group_ids" parameters, and a valid boolean value is required for "assign_public_ip"')

            network_configuration={
                'awsvpcConfiguration': {
                    'subnets': subnet_ids,
                    'securityGroups': security_group_ids,
                    'assignPublicIp': ('DISABLED', 'ENABLED')[assign_public_ip]
                }
            }

        if overrides is None:
            overrides = {}

        return self.__client__.run_task(
            cluster=cluster.get_arn(),
            taskDefinition = task_definition.get_arn(),
            launchType=launch_type,
            count=count,
            platformVersion=platform_version,
            networkConfiguration=network_configuration,
            overrides=overrides
        )

from abc import abstractmethod
from Aws.Lambda.Log import Log
from typing import Optional, Any


class Function:
    """
    Lambda function boilerplate
    """

    def __init__(self, aws_event=None, aws_context=None, credential=None):
        """
        :param aws_event: AWS Lambda uses this parameter to pass in event data to the handler
        :type aws_event: Optional[dict]

        :param aws_context: AWS Lambda uses this parameter to provide runtime information to your handler, or None if executed via CLI
        :type aws_context: Optional[LambdaContext]

        :param credential: Optional credential to user for authentication via CLI
        :type credential: Optional[Credential]
        """
        self.__aws_event__ = aws_event
        self.__aws_context__ = aws_context
        self.__credential__ = credential
        self.__return__ = None

        # Set lambda function name
        Log.set_function_name(self.get_aws_function_name())

        # Set logging level
        if self.__aws_context__ is None:
            Log.warning('No AWS context available, this is only normal if testing the function via CLI')

        if 'log_level' in self.__aws_event__:
            print('Retrieving requested logging level from Lambda function parameters...')
            try:
                log_level = int(self.__aws_event__['log_level'])
                print('Requested logging level: {log_level}'.format(log_level=Log.get_log_level_name(log_level)))
                Log.set_level(log_level)
            except Exception as log_exception:
                print('An unexpected error occurred while attempting to set desired logging level.')
                raise Exception(log_exception)
        else:
            Log.set_level(Log.LEVEL_TRACE)

        try:
            Log.trace('Executing user initialization function...')
            self.init()
        except Exception as init_exception:
            # Something went wrong inside the users init function- log the error
            Log.error('Unhandled exception during execution of user initialization function:\n{init_exception}'.format(init_exception=init_exception))
            raise init_exception

        try:
            Log.trace('Executing user run function...')
            self.set_return_value(self.run())
        except Exception as run_exception:
            # Something went wrong inside the users run function- log the error
            Log.error('Unhandled exception during execution of user run function:\n{run_exception}'.format(run_exception=run_exception))
            raise run_exception

        # Execution completed, log out the time remaining- this may be useful for tracking bloat/performance degradation over the life of the Lambda function
        time_remaining = self.get_aws_time_remaining()

        if time_remaining is not None:
            Log.info('Execution completed with {time_remaining} seconds remaining'.format(time_remaining=float(time_remaining) / 1000))

    def set_return_value(self, value) -> None:
        """
        Set lambda return value

        :param value: The return value
        :type value: Any
        """
        self.__return__ = value

    def get_return_value(self) -> Any:
        """
        Get lambda return value

        :return: Lambda return value
        """
        return self.__return__

    @abstractmethod
    def init(self) -> None:
        """
        This function should be overridden with code to be executed prior to running the main run function
        """
        pass

    @abstractmethod
    def run(self) -> Any:
        """
        This function should be overridden with the main application code
        """
        pass

    def get_aws_context(self) -> Any:
        """
        Return the AWS event context

        :return: AWS context, or None if not set
        """
        return self.__aws_context__

    def get_aws_event(self) -> Optional[dict]:
        """
        Return the AWS event parameter

        :return: AWS event, or None if not set
        """
        return self.__aws_event__

    def get_aws_event_parameter(self, parameter) -> Optional[str]:
        """
        Return the AWS event parameter

        :return: Event parameter, or None if not set
        """
        if parameter not in self.__aws_event__:
            return None

        return self.__aws_event__[parameter]

    def get_aws_request_id(self) -> Optional[str]:
        """
        Get the unique AWS request ID

        :return: AWS request ID, or None if executed via CLI
        """
        if self.__aws_context__ is None:
            return None

        return self.__aws_context__.aws_request_id

    def get_aws_function_arn(self) -> Optional[str]:
        """
        Return the ARN of the AWS function being executed

        :return: AWS lambda function ARN, or None if executed via CLI
        """
        if self.__aws_context__ is None:
            return None

        return self.__aws_context__.invoked_function_arn

    def get_aws_function_name(self) -> Optional[str]:
        """
        Return the name of the AWS function being executed

        :return: AWS lambda function name, or None if executed via CLI
        """
        if self.__aws_context__ is None:
            return None

        return self.__aws_context__.function_name

    def get_aws_time_remaining(self) -> Optional[str]:
        """
        Return the number of milliseconds remaining before the Lambda times out

        :return: Number of milliseconds remaining, or None if executed via CLI
        """
        if self.__aws_context__ is None:
            return None

        return self.__aws_context__.get_remaining_time_in_millis()

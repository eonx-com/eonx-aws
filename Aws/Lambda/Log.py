import inspect
import os

from time import strftime


class Log:
    # Logging history
    __history__ = []

    # Logging level
    __level__ = None

    # Optional function name to append to log
    __function_name__ = None

    # Logging level constants
    LEVEL_EXCEPTION = -2
    LEVEL_TEST = -1
    LEVEL_ERROR = 0
    LEVEL_INFO = 1
    LEVEL_WARNING = 2
    LEVEL_DEBUG = 3
    LEVEL_TRACE = 4

    @staticmethod
    def set_function_name(function_name) -> None:
        """
        Set function name for prefixing in log

        :return: None
        """
        Log.__function_name__ = function_name

    @staticmethod
    def set_level(level) -> None:
        """
        Set logging display level

        :type level: int
        :param level: Logging level, one of the LEVEL class constants

        :return: None
        """
        if level not in (Log.LEVEL_EXCEPTION, Log.LEVEL_TEST, Log.LEVEL_ERROR, Log.LEVEL_INFO, Log.LEVEL_WARNING, Log.LEVEL_DEBUG, Log.LEVEL_TRACE):
            raise Exception('Unknown logging level specified')

        Log.__level__ = level

    @staticmethod
    def info(message) -> None:
        """
        Info level logging function

        :type message: str or Exception
        :param message: The message to be logged

        :return: None
        """
        # This has to be the first line in the function otherwise this will return the wrong stack frame
        stack_frame = inspect.stack()[1]

        Log.log(
            level=Log.LEVEL_INFO,
            stack_frame=stack_frame,
            message=message
        )

    @staticmethod
    def error(message) -> None:
        """
        Error level logging function

        :param message: Message to print
        :type message: str/Exception

        :return: None
        """
        # This has to be the first line in the function otherwise this will return the wrong stack frame
        stack_frame = inspect.stack()[1]

        Log.log(
            level=Log.LEVEL_ERROR,
            stack_frame=stack_frame,
            message=message
        )

    @staticmethod
    def warning(message) -> None:
        """
        Warning level logging function

        :param message: Message to print
        :type message: str/Exception

        :return: None
        """
        # This has to be the first line in the function otherwise this will return the wrong stack frame
        stack_frame = inspect.stack()[1]

        Log.log(
            level=Log.LEVEL_WARNING,
            stack_frame=stack_frame,
            message=message
        )

    @staticmethod
    def debug(message) -> None:
        """
        Debug level logging function

        :param message: Message to print
        :type message: str/Exception

        :return: None
        """
        # This has to be the first line in the function otherwise this will return the wrong stack frame
        stack_frame = inspect.stack()[1]

        Log.log(
            level=Log.LEVEL_DEBUG,
            stack_frame=stack_frame,
            message=message
        )

    @staticmethod
    def test(message) -> None:
        """
        Unit test level logging function

        :param message: Message to print
        :type message: str/Exception

        :return: None
        """
        # This has to be the first line in the function otherwise this will return the wrong stack frame
        stack_frame = inspect.stack()[1]

        Log.log(
            level=Log.LEVEL_TEST,
            stack_frame=stack_frame,
            message=message
        )

    @staticmethod
    def trace(message) -> None:
        """
        Trace level logging function

        :param message: Message to print
        :type message: str/Exception

        :return: None
        """
        # This has to be the first line in the function otherwise this will return the wrong stack frame
        stack_frame = inspect.stack()[1]

        Log.log(
            level=Log.LEVEL_TRACE,
            stack_frame=stack_frame,
            message=message
        )

    @staticmethod
    def exception(message, base_exception=None) -> None:
        """
        Exception error logging function

        :type message: str
        :param message: Message to print

        :type base_exception: Exception or str or None
        :param base_exception: The exception error that was raised

        :return: None
        """
        # This has to be the first line in the function otherwise this will return the wrong stack frame
        stack_frame = inspect.stack()[1]

        Log.log(
            level=Log.LEVEL_EXCEPTION,
            stack_frame=stack_frame,
            message=message
        )

        Log.log(
            level=Log.LEVEL_EXCEPTION,
            stack_frame=stack_frame,
            message=base_exception
        )

    @staticmethod
    def get_log_level_name(level) -> str:
        """
        Retrieve the name fo the logging level

        :type level: int
        :param level: The levels integer ID

        :return: The name of the logging level
        """
        if level == Log.LEVEL_TEST:
            level_name = 'TEST'
        elif level == Log.LEVEL_ERROR:
            level_name = 'ERROR'
        elif level == Log.LEVEL_EXCEPTION:
            level_name = 'EXCEPTION'
        elif level == Log.LEVEL_INFO:
            level_name = 'INFO'
        elif level == Log.LEVEL_WARNING:
            level_name = 'WARNING'
        elif level == Log.LEVEL_DEBUG:
            level_name = 'DEBUG'
        elif level == Log.LEVEL_TRACE:
            level_name = 'TRACE'
        else:
            raise Exception('Unknown logging level specified')

        return level_name

    @staticmethod
    def log(level, message, stack_frame=None) -> None:
        # If the message is multi-line, split it out and post each one individually
        lines = str(message).split('\n')
        if len(lines) > 1:
            for line in lines:
                if len(line.strip()) > 0:
                    Log.log(level=level, message=line, stack_frame=stack_frame)
            return

        # If no logging level is defined, select one based on the current context
        if Log.__level__ is None:
            # Work out if we are in a unit test
            current_stack = inspect.stack()
            is_unit_test = False
            for stack_frame in current_stack:
                for program_line in stack_frame[4]:
                    if "unittest" in program_line:
                        is_unit_test = True
                        break

            if is_unit_test is True:
                # Running unit tests, disable logging
                print('Running unit tests, logging test messages only...', flush=True)
                Log.__level__ = Log.LEVEL_TEST
            else:
                # Not running unit tests, default to maximum logging level
                print('No logging level has been defined, defaulting to maximum logging...', flush=True)
                Log.__level__ = Log.LEVEL_TRACE

        # Retrieve current timestamp
        timestamp = strftime("%Y-%m-%d %H:%M:%S")

        # Create history entry
        history = {
            'message': message,
            'message_formatted': '',
            'level': level,
            'timestamp': timestamp,
            'filename': '',
            'function': '',
            'line_number': '',
        }

        message_formatted = Log.format_message(level=level, timestamp=timestamp, message=message, stack_frame=stack_frame)

        history['message_formatted'] = message_formatted

        if stack_frame is not None:
            history['filename'] = stack_frame.filename
            history['function'] = stack_frame.function
            history['line_number'] = stack_frame.lineno

        # Display the message if appropriate based on the current log level
        if Log.__level__ is None or Log.__level__ >= level:
            print(message_formatted, flush=True)

        # Add entry to the log
        Log.__history__.append(history)

    @staticmethod
    def format_message(level, message, timestamp, stack_frame=None) -> str:
        # Convert the log level to a human readable string
        level_name = Log.get_log_level_name(level)

        # Trim whitespace off the message
        message = str(message).strip()

        # Create a display formatted version of the message
        message_formatted = '{timestamp}'.format(timestamp=timestamp).ljust(19)

        if Log.__function_name__ is not None:
            message_formatted = "{message_formatted} [{function}]".format(function=Log.__function_name__, message_formatted=message_formatted)

        # If we received a stack frame, add its details to the log entry
        if stack_frame is not None:
            message_formatted = '{message_formatted} [{filename}:{function}:{line_number}]'.format(
                level_name=level_name,
                filename=os.path.basename(stack_frame.filename),
                function=stack_frame.function,
                line_number=stack_frame.lineno,
                message_formatted=message_formatted
            )

        message_formatted = '{message_formatted} {level_name}: {message}'.format(message_formatted=message_formatted, level_name=level_name, message=message)

        return message_formatted

    @staticmethod
    def clear_log_history() -> None:
        """
        Clear any existing log history

        :return: None
        """
        Log.__history__ = []

    @staticmethod
    def get_log_history(self) -> list:
        """
        Return the complete log history regardless of the current log level

        :return: list
        """
        return self.__history__

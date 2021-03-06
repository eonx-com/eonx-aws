from Aws.Lambda.Log import Log


class Iterator:
    @staticmethod
    def iterate(client, method_name, data_key, arguments={}, token_key_next='nextToken', token_key_write='nextToken') -> list:
        """
        Call an AWS client method and iterate to retrieve all available results

        :param client: Boto3 client used to perform the action
        :type client: Object

        :param method_name: Boto3 method name to call
        :type method_name: str

        :param arguments: Dictionary of arguments to be passed to method
        :type arguments: dict

        :param data_key: The key in the AWS results that contains the response data
        :type data_key: str

        :param token_key_next: The key in the AWS results that contains the pagination token
        :type token_key_next: str

        :param token_key_write: The key in the AWS results that contains to write back on subsequent calls
        :type token_key_write: str

        :return: List of results
        
        :raises Exception: if the method does not return expected dictionary type
        """
        method_to_call = getattr(client, method_name)

        result = method_to_call(**arguments)

        if isinstance(result, dict) is False:
            raise Exception('Unexpected result received')

        return_list = []

        if data_key not in result.keys():
            return return_list

        while True:
            # If there is nothing left- get out of here
            if len(result[data_key]) == 0:
                break

            return_list.extend(result[data_key])

            # Check if there are any more results to retrieve
            if token_key_next not in result.keys() or result[token_key_next] is None:
                break

            # Add pagination token to next method call and get next page of results
            arguments[token_key_write] = result[token_key_next]
            result = method_to_call(**arguments)

        # Return the results we found
        return return_list

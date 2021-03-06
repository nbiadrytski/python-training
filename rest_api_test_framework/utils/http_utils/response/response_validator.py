from rest_api_test_framework.utils.config_parser import DataConfigParser
from rest_api_test_framework.utils.funcs import *
import logging


class ResponseValidator:
    """
    Validate HTTP response using requests module and helper funcs.
    Log request status code, response headers and response body when ResponseValidator object is created.

    Parameters:
        resp (Response): Response object returned by HTTP request.
    """

    def __init__(self, resp):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f'STATUS CODE: {resp.status_code}\n')
        self.logger.info(f'RESPONSE HEADERS: {resp.headers}\n')
        self.logger.info(f'RESPONSE BODY: {resp.text}\n')

    @staticmethod
    def get_status_code(resp):
        """
        Get status code of HTTP request.

        Parameters:
            resp (Response): Response object returned by HTTP request.

        Returns:
            int: HTTP status code
        """
        status_code = resp.status_code
        return status_code

    @staticmethod
    def get_response_header(resp, header_name):
        """
        Get response header of HTTP request.

        Parameters:
            resp (Response): Response object returned by HTTP request.
            header_name (str): response header name

        Returns:
            str: response header value
        """
        response_header = resp.headers[header_name]
        return response_header

    @staticmethod
    def get_value_from_json(resp, json_path):
        """
        Get JSON key value by provided json path.

        Parameters:
            resp (Response): Response object returned by HTTP request.
            json_path (str): path to JSON key

        Returns:
            str: JSON key value
        """
        actual_json = resp.json()
        value = find_item_by_jsonpath(actual_json, json_path)
        return value

    @staticmethod
    def response_equals(actual_response, expected_response):
        """
        Compare actual HTTP response in plain text with expected response stored as str in .txt file

        Parameters:
            actual_response (Response): Response object returned by HTTP request.
            expected_response (str): relative path to txt file with expected

        Returns:
            bool: True if actual_response has the same content as expected_response, otherwise False
        """
        expected_response = file_content(expected_response)
        return actual_response.text == expected_response

    @staticmethod
    def contains(resp):
        """
        Get response as text.

        Parameters:
            resp (Response): Response object returned by HTTP request.

        Returns:
            str: response as text
        """
        text_response = resp.text
        return text_response

    @staticmethod
    def json_response_equals(actual_response,
                             expected_response,
                             config_section_title,
                             ignore_keys=()):
        """
        Check if actual JSON response has the same content as expected response stored in .json file.
        1. Get json_keys_config.ini by creating DataConfigParser object (provide path to config file)
        2. Convert actual json response to dict
        3. Convert expected json response from .json file to dict
        4. Compare 2 dicts and log diff if they do not match

        Parameters:
            actual_response (Response): Response object returned by HTTP request.
            expected_response (str): path to .json file with stored expected response
            config_section_title (str): name of config.ini section
            ignore_keys (tuple): optional, a tuple of config.ini keys to be ignored when comparing responses

        Returns:
            bool: whether actual and expected responses match
        """
        config_parser = DataConfigParser('resources/data_configs/json_keys_config.ini')
        ignored_keys = config_parser.get_ignored_keys(config_section_title, ignore_keys)
        actual_response = actual_response.json()
        expected_response = convert_json_to_dict(expected_response)
        responses_match = compare_dicts(actual_response, expected_response, ignored_keys)
        return responses_match




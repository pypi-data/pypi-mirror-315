import ast
import base64
import json
import os
import time
import requests
import logging
from typing import Any, Dict, List, Type
from io import BufferedReader, BytesIO, TextIOWrapper
from pydantic import BaseModel

from .ai_config import AIConfig
from .ai_provider import *
from .exceptions import *

logger = logging.getLogger(__name__)

class QueryType(Enum):
    DIRECT = 0,
    RAG = 1,
    RDBMS = 2,
    FUNCTION = 3

class AIClient:
    _LOOKUP_ENDPOINT: str = 'https://api.jellyfaas.com/auth-service/v1/lookup'
    _QUERY_SERVICE_ENDPOINT: str = 'https://ai.jellyfaas.com/query-service/v1'
    _HEADER_API_KEY:      str = "x-jf-apikey"
    _HEADER_TOKEN: str = 'jfwt'

    _config: AIConfig = None
    _query_type: QueryType = QueryType.DIRECT
    

    # Funciton calling querying
    _functions = []

    # Vector DB querying
    _vector_database_name = None
    _vector_database_connection_string = None

    # RDBMS querying
    _rdbms_tables = None
    _rdbms_connection_string = None


    def __init__(self, config: AIConfig) -> None:      
        """
        Initializes and authenticates the AIClient with the provided config object.

        :param config A JellyFAAS AIClient config object.

        :raises AuthenticationFailedException If authentication fails.
        """
        if not isinstance(config, AIConfig):
            raise JellyFaasException('Invalid parameter: config must be of type \'jellyfaas.Config\'')
        
        if not config.is_authenticated:
            raise JellyFaasException('Invalid config object: unauthenticated')
        
        self._config = config
    
    def lookup_function(self, function):
        if type(function) != dict:
            raise JellyFaasException('Expected function dict')
        function_id = function.get('id', None)
        if function_id == None:
            raise JellyFaasException('Expected function id')
        query_params = {
            'id': function_id
        }
        function_version = function.get('version', None)
        if function_version != None:
            query_params['version'] = function_version

        self.__print_debug(f"Starting lookup_function method with function_id={function_id}")
        
        try:
            lookup_response = requests.get(
                self._LOOKUP_ENDPOINT,
                headers={self._HEADER_API_KEY: self._config._api_key},
                params=query_params
            )
            
            self.__print_debug(f"Received response: {lookup_response.status_code}")
            lookup_response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
            lookup_response_json = lookup_response.json()  # Parse the response as a JSON string
            self.__print_debug(f"Response JSON: {lookup_response_json}")

            function_details = {
                    'id': function_id,
                    'version': function_version,
                    'dns': lookup_response_json.get("dns", None),
                    'requirements': lookup_response_json.get("requirements", None)
                }
            
            self._functions.append(function_details)
            self._query_type = QueryType.FUNCTION
            self.__print_debug("Successfully looked up function")

            return self

        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            logger.error(error_message)
            raise FunctionLookupException(error_message)
        except Exception as err:
            error_message = f"Other error occurred: {err}"
            logger.error(error_message)
            raise FunctionLookupException(f"Other error occurred: {err}")

    def connect_vector_database(self, database_name, connection_string = None):
        if database_name == None:
            raise JellyFaasException('Invalid database name')
        
        self._vector_database_name = database_name
        if connection_string != None:
            self._vector_database_connection_string = connection_string
        
        self._query_type = QueryType.RAG
        return self

    def connect_relational_database(self, connection_string:str, tables:List[str]):
        if (connection_string == ''):
            raise JellyFaasException('Invalid connection string')
        
        if (tables == None):
            raise JellyFaasException('Invalid tables')
        
        
        self._rdbms_connection_string = connection_string
        self._rdbms_tables = tables
        self._query_type = QueryType.RDBMS
        return self
    

    def query(self, query, rag_query=None, rdbms_query=None):

        match (self._query_type):
            case QueryType.DIRECT:
                return self._direct_query(query)
            case QueryType.RAG:
                return self._vector_query(query, rag_query)
            case QueryType.RDBMS:
                return self._rdbms_query(query, rdbms_query)
            case QueryType.FUNCTION:
                return self._function_query(query)
    
    def _function_query(self, query):
        # Prepare the request body
        request_body = {
            "query": query,
            "function": self._functions[0]['id'],
            "ai_platform": "gemini"
        }
        # Make the request to the 'query-vectordb' API
        try:
            headers = {self._HEADER_TOKEN: self._config._token}
            response = requests.post(
                url=self._QUERY_SERVICE_ENDPOINT+'/function',
                headers=headers,
                json=request_body
            )
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")
    

    def _direct_query(self, query):
        # Prepare the request body
        request_body = {
            "query": query
        }
        # Make the request to the 'query-vectordb' API
        try:
            headers = {self._HEADER_TOKEN: self._config._token}
            response = requests.post(
                url=self._QUERY_SERVICE_ENDPOINT+'/query',
                headers=headers,
                json=request_body
            )

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")
        
    def _vector_query(self, query, rag_query=None):

        # Prepare the request body
        request_body = {
            "query": query,
            "vector_mongo_collection": self._vector_database_name
        }

        if self._vector_database_connection_string:
            request_body["vector_mongo_connection_string"] = self._vector_database_connection_string

        if rag_query:
            request_body["rag_query"] = rag_query

        # Make the request to the 'query-vectordb' API
        try:
            headers = {self._HEADER_TOKEN: self._config._token}
            response = requests.post(
                url=self._QUERY_SERVICE_ENDPOINT+'/vectordb',
                headers=headers,
                json=request_body
            )

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")
    
    def _rdbms_query(self, query, rdbms_query=None):

        # Prepare the request body
        request_body = {
            "query": query,
            "tables": self._rdbms_tables,
            "mysql_connection_string": self._rdbms_connection_string
        }

        # Optional RAG query
        if rdbms_query:
           request_body["rdbms_query"] = rdbms_query

        # Make the request to the 'query-vectordb' API
        try:
            headers = {self._HEADER_TOKEN: self._config._token}
            response = requests.post(
                url=self._QUERY_SERVICE_ENDPOINT+'/rdbms',
                headers=headers,
                json=request_body
            )

            result = response.json()
            if response.status_code == 200:
                return result
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")

    def upload(self, file, database_name, blocking=True):
        try:
            print(f'Uploading file(s)...')
            headers = {"jfwt": self._token}
            response = requests.post(
                url='https://ai.jellyfaas.com/embedder-service/v1/upload',
                params={
                    'collection_name': database_name
                },
                headers=headers,
                files={
                    'file': file
                }
            )

            if response.status_code != 202:
                raise Exception(f"Error {response.status_code}: {response.text}")
           
            result = response.json()
            upload_id = result['upload_id']

            print('Upload finished')

            if blocking == False:
                return upload_id
        
            print('Embedding file(s)...')

            while(True):
                status = self.get_upload_status(upload_id)
                if status['status'] == 'completed':
                    break
                time.sleep(1)
            
            print('File successfully embedded')

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")
    
    def get_upload_status(self, id):
        try:
            
            headers = {"jfwt": self._token}
            response = requests.get(
                url='https://ai.jellyfaas.com/embedder-service/v1/status',
                params={
                    'upload_id': id
                },
                headers=headers,
            )

            if response.status_code == 200:
                result = response.json()
                if self._do_debug:
                    self.__print_debug(f"Response: {json.dumps(result, indent=2)}")
                return result
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")
    
    def connect_sql_database(self, connection_string, tables):
        self._rdbms_connection_string = connection_string
        self._rdbms_tables = tables
        return self

    def reset(self):
        self._rdbms_connection_string = None
        self._rdbms_tables = None
        self.connect_vector_database('')
        return self
    
    def __print_debug(self, msg):
        """
        Log a debug message.

        :param msg (str) The message to log.
        """
        if (not hasattr(self, '_config')) or self._config == None: logger.debug(msg)
        elif self._config._do_debug: logger.debug(msg)
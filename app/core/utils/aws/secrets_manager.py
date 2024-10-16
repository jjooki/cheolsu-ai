import json
import logging

from .base import AWS

class SecretsManager(AWS):
    def __init__(self,
                 aws_access_key_id: str=None,
                 aws_secret_access_key: str=None,
                 region_name: str=None):
        ## `secretmanager:GetSecretValue` IAM role is required to run this code
        super().__init__(aws_access_key_id,
                         aws_secret_access_key,
                         region_name)
        self.client = self.session.client("secretsmanager")

    # snippet-end:[python.example_code.python.GetSecretValue.decl]

    def get_secret(self, secret_name):
        """
        Retrieve individual secrets from AWS Secrets Manager using the get_secret_value API.
        This function assumes the stack mentioned in the source code README has been successfully deployed.
        This stack includes 7 secrets, all of which have names beginning with "mySecret".

        :param secret_name: The name of the secret fetched.
        :type secret_name: str
        """
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
            logging.info("Secret retrieved successfully.")
            secret = get_secret_value_response["SecretString"]
            return json.loads(secret)
        
        except self.client.exceptions.ResourceNotFoundException:
            msg = f"The requested secret {secret_name} was not found."
            logging.info(msg)
            return msg
        
        except Exception as e:
            logging.error(f"Error retrieving secret: {e}")
            raise e
import os

from hubaxle_api_client import api, models
from hubaxle_api_client.api_client import ApiClient
from hubaxle_api_client.configuration import Configuration


class GLHub:
    """
    Convenience class for accessing the GLHub API, modeled after the Groundlight Python SDK
    This code does NOT auto track changes to the GLHub API
    """

    def _error_param_not_set(self, param, param_name):
        if param is None:
            raise ValueError(
                f"{param_name} was not provided or found in the environment variables. "
                "Please provide it as a parameter or set it in the environment variables."
            )

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        hubid: str | None = None,
        endpoint: str | None = None,
    ):
        username = username or os.environ.get("GLHUB_USERNAME")
        # TODO require auth once it is available for app users
        # self._error_param_not_set(username, 'username')
        password = password or os.environ.get("GLHUB_PASSWORD")
        # self._error_param_not_set(password, 'password')

        hubid = hubid or os.environ.get("GLHUB_HUBID")
        # initialize with endpoint pointing to localhost to reach hubaxle from an app running on the device
        # endpoint = "http://localhost:80/"
        if not endpoint:
            self.endpoint = f"https://{hubid}.hub.groundlight-devices.com"
        else:
            self.endpoint = endpoint

        self.configuration = Configuration(host=self.endpoint)
        self.configuration.username = username
        self.configuration.password = password

        self.api_client = ApiClient(configuration=self.configuration)
        self.secrets_api = api.SecretsApi(api_client=self.api_client)
        self.app_configs_api = api.AppDataApi(api_client=self.api_client)
        self.cameras_api = api.CamerasApi(api_client=self.api_client)

    def list_secrets(self):
        """
        List all secrets in the hub
        """
        return self.secrets_api.list_secrets()

    def create_secret(self, secret_name: str, secret_value: str):
        """
        Create a secret in the hub
        """
        secret = models.SecretRequest(name=secret_name, value=secret_value)
        return self.secrets_api.create_secret(secret)

    def get_app_config(self):
        """
        Get the app configuration
        """
        return self.app_configs_api.get_app_config()

    def set_app_config(self, **kwargs):
        """
        Set the app configuration
        """
        config = models.ConfigEntryRequest.from_dict(kwargs)
        return self.app_configs_api.put_app_config(config)

    def list_cameras(self):
        """
        Get a list of all cameras accessible to the current user
        """
        return self.cameras_api.list_cameras()

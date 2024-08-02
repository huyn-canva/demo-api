import openapi_client

from auth import Auth


class CanvaClient():
    configuration:openapi_client.Configuration
    _client: openapi_client.ApiClient

    def __init__(self, auth: Auth):
        self.configuration = openapi_client.Configuration(
            host="https://api.canva.com/rest",
            access_token=auth.access_token,
        )
        self._client=openapi_client.ApiClient(self.configuration)

    def get_design_api(self) -> openapi_client.DesignApi:
        return openapi_client.DesignApi(self._client)

import openapi_client
from typing import Optional



configuration = openapi_client.Configuration(
    host="https://api.canva.com/rest"
)



def get_api_client() -> openapi_client.ApiClient:
    return openapi_client.ApiClient(configuration)


def get_design_api(client: openapi_client.ApiClient) -> openapi_client.DesignApi:
    return openapi_client.DesignApi(client)
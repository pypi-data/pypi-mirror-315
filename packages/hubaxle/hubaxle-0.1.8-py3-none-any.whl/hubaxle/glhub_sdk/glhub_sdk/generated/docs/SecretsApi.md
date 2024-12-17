# hubaxle_api_client.SecretsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_secret**](SecretsApi.md#create_secret) | **POST** /api/v1/secrets | 
[**list_secrets**](SecretsApi.md#list_secrets) | **GET** /api/v1/secrets | 


# **create_secret**
> Secret create_secret(secret_request)



Create a secret in the hub

### Example

* Basic Authentication (basicAuth):

```python
import hubaxle_api_client
from hubaxle_api_client.models.secret import Secret
from hubaxle_api_client.models.secret_request import SecretRequest
from hubaxle_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hubaxle_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = hubaxle_api_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with hubaxle_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hubaxle_api_client.SecretsApi(api_client)
    secret_request = hubaxle_api_client.SecretRequest() # SecretRequest | 

    try:
        api_response = api_instance.create_secret(secret_request)
        print("The response of SecretsApi->create_secret:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->create_secret: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **secret_request** | [**SecretRequest**](SecretRequest.md)|  | 

### Return type

[**Secret**](Secret.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_secrets**
> List[Secret] list_secrets()



List all secrets in the hub

### Example

* Basic Authentication (basicAuth):

```python
import hubaxle_api_client
from hubaxle_api_client.models.secret import Secret
from hubaxle_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hubaxle_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = hubaxle_api_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with hubaxle_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hubaxle_api_client.SecretsApi(api_client)

    try:
        api_response = api_instance.list_secrets()
        print("The response of SecretsApi->list_secrets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->list_secrets: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Secret]**](Secret.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


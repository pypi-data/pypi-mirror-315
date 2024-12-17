# hubaxle_api_client.AppDataApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_app_config**](AppDataApi.md#get_app_config) | **GET** /api/v1/appdata/app/appconfig | 
[**patch_app_config**](AppDataApi.md#patch_app_config) | **PATCH** /api/v1/appdata/app/appconfig | 
[**put_app_config**](AppDataApi.md#put_app_config) | **PUT** /api/v1/appdata/app/appconfig | 


# **get_app_config**
> ConfigEntry get_app_config()



Get the app configuration, returned as a binary stream

### Example

* Basic Authentication (basicAuth):

```python
import hubaxle_api_client
from hubaxle_api_client.models.config_entry import ConfigEntry
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
    api_instance = hubaxle_api_client.AppDataApi(api_client)

    try:
        api_response = api_instance.get_app_config()
        print("The response of AppDataApi->get_app_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AppDataApi->get_app_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ConfigEntry**](ConfigEntry.md)

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

# **patch_app_config**
> ConfigEntry patch_app_config(patched_config_entry_request=patched_config_entry_request)



patch the app configuration

### Example

* Basic Authentication (basicAuth):

```python
import hubaxle_api_client
from hubaxle_api_client.models.config_entry import ConfigEntry
from hubaxle_api_client.models.patched_config_entry_request import PatchedConfigEntryRequest
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
    api_instance = hubaxle_api_client.AppDataApi(api_client)
    patched_config_entry_request = hubaxle_api_client.PatchedConfigEntryRequest() # PatchedConfigEntryRequest |  (optional)

    try:
        api_response = api_instance.patch_app_config(patched_config_entry_request=patched_config_entry_request)
        print("The response of AppDataApi->patch_app_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AppDataApi->patch_app_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **patched_config_entry_request** | [**PatchedConfigEntryRequest**](PatchedConfigEntryRequest.md)|  | [optional] 

### Return type

[**ConfigEntry**](ConfigEntry.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_app_config**
> ConfigEntry put_app_config(config_entry_request)



put the app configuration

### Example

* Basic Authentication (basicAuth):

```python
import hubaxle_api_client
from hubaxle_api_client.models.config_entry import ConfigEntry
from hubaxle_api_client.models.config_entry_request import ConfigEntryRequest
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
    api_instance = hubaxle_api_client.AppDataApi(api_client)
    config_entry_request = hubaxle_api_client.ConfigEntryRequest() # ConfigEntryRequest | 

    try:
        api_response = api_instance.put_app_config(config_entry_request)
        print("The response of AppDataApi->put_app_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AppDataApi->put_app_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **config_entry_request** | [**ConfigEntryRequest**](ConfigEntryRequest.md)|  | 

### Return type

[**ConfigEntry**](ConfigEntry.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


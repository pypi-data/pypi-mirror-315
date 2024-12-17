# SecretRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**value** | **str** |  | 

## Example

```python
from hubaxle_api_client.models.secret_request import SecretRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SecretRequest from a JSON string
secret_request_instance = SecretRequest.from_json(json)
# print the JSON string representation of the object
print(SecretRequest.to_json())

# convert the object into a dict
secret_request_dict = secret_request_instance.to_dict()
# create an instance of SecretRequest from a dict
secret_request_form_dict = secret_request.from_dict(secret_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



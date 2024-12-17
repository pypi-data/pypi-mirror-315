# ConfigEntryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | [**KindEnum**](KindEnum.md) |  | 
**contents** | **str** |  | 

## Example

```python
from hubaxle_api_client.models.config_entry_request import ConfigEntryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigEntryRequest from a JSON string
config_entry_request_instance = ConfigEntryRequest.from_json(json)
# print the JSON string representation of the object
print(ConfigEntryRequest.to_json())

# convert the object into a dict
config_entry_request_dict = config_entry_request_instance.to_dict()
# create an instance of ConfigEntryRequest from a dict
config_entry_request_form_dict = config_entry_request.from_dict(config_entry_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



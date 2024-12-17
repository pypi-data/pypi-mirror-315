# PatchedConfigEntryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | [**KindEnum**](KindEnum.md) |  | [optional] 
**contents** | **str** |  | [optional] 

## Example

```python
from hubaxle_api_client.models.patched_config_entry_request import PatchedConfigEntryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedConfigEntryRequest from a JSON string
patched_config_entry_request_instance = PatchedConfigEntryRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedConfigEntryRequest.to_json())

# convert the object into a dict
patched_config_entry_request_dict = patched_config_entry_request_instance.to_dict()
# create an instance of PatchedConfigEntryRequest from a dict
patched_config_entry_request_form_dict = patched_config_entry_request.from_dict(patched_config_entry_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



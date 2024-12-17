# ConfigEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [readonly] 
**name** | **str** |  | [readonly] 
**kind** | [**KindEnum**](KindEnum.md) |  | 
**contents** | **str** |  | 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 

## Example

```python
from hubaxle_api_client.models.config_entry import ConfigEntry

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigEntry from a JSON string
config_entry_instance = ConfigEntry.from_json(json)
# print the JSON string representation of the object
print(ConfigEntry.to_json())

# convert the object into a dict
config_entry_dict = config_entry_instance.to_dict()
# create an instance of ConfigEntry from a dict
config_entry_form_dict = config_entry.from_dict(config_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



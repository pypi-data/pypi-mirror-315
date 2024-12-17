# CameraConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [readonly] 
**name** | **str** |  | 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**rtsp_url** | **str** |  | 
**kind** | [**KindEnum**](KindEnum.md) |  | 
**contents** | **str** |  | 

## Example

```python
from hubaxle_api_client.models.camera_config import CameraConfig

# TODO update the JSON string below
json = "{}"
# create an instance of CameraConfig from a JSON string
camera_config_instance = CameraConfig.from_json(json)
# print the JSON string representation of the object
print(CameraConfig.to_json())

# convert the object into a dict
camera_config_dict = camera_config_instance.to_dict()
# create an instance of CameraConfig from a dict
camera_config_form_dict = camera_config.from_dict(camera_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



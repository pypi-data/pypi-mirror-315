from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric import Metric


T = TypeVar("T", bound="ResourceDeploymentMetricsInferencePerRegionType0")


@_attrs_define
class ResourceDeploymentMetricsInferencePerRegionType0:
    """Historical requests (in last 24 hours) per location, for the model deployment

    Attributes:
        region (Union[Unset, List['Metric']]): Array of metrics
    """

    region: Union[Unset, List["Metric"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        region: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.region, Unset):
            region = []
            for componentsschemas_array_metric_item_data in self.region:
                componentsschemas_array_metric_item = (
                    componentsschemas_array_metric_item_data.to_dict()
                )
                region.append(componentsschemas_array_metric_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric import Metric

        d = src_dict.copy()
        region = []
        _region = d.pop("region", UNSET)
        for componentsschemas_array_metric_item_data in _region or []:
            componentsschemas_array_metric_item = Metric.from_dict(
                componentsschemas_array_metric_item_data
            )

            region.append(componentsschemas_array_metric_item)

        resource_deployment_metrics_inference_per_region_type_0 = cls(
            region=region,
        )

        resource_deployment_metrics_inference_per_region_type_0.additional_properties = d
        return resource_deployment_metrics_inference_per_region_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

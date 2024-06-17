from typing import Optional, Union

from pydantic import RootModel

from .base_model import BaseModel
from . import response as response_models

MODEL_TYPE = "geographic_areas"


class APIGeoAreaFields(BaseModel):
    area_name: Optional[str] = None
    area_type: Optional[str] = None
    city_radius: Optional[int] = 20
    polygon_coordinates: Optional[str] = None
    assigned_rse_name: Optional[str] = None
    hub_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geocode: Optional[dict] = None
    auto_response_email_templates: Optional[list[str]] = None


class APIGeoAreaRelationships(BaseModel):
    hub: Optional[response_models.APILinksAndData] = None
    assigned_rse: Optional[response_models.APILinksAndData] = None
    auto_response_email_templates: Optional[list[response_models.APILinksAndData]] = None


class APIGeoAreaData(response_models.APIData):
    fields: APIGeoAreaFields


class ListAPIGeoAreaData(RootModel):
    root: list[APIGeoAreaData]


class APIGeoAreaResponse(response_models.APIResponse):
    data: APIGeoAreaData


class ListAPIGeoAreaResponse(response_models.ListAPIResponse):
    data: list[Union[APIGeoAreaData, dict]]

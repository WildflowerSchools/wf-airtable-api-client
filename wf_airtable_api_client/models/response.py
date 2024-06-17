from typing import Any, Optional, Union

from pydantic import field_validator

from .base_model import BaseModel

APILinksType = dict[str, Optional[str]]


class APILinks(BaseModel):
    links: Optional[APILinksType] = None


class APIDataBase(BaseModel):
    id: str
    type: str


class APIDataWithFields(BaseModel):
    id: str
    type: str
    fields: dict

    @field_validator("fields", mode="before")
    @classmethod
    def transform_fields(cls, v: Any):
        return dict(v)


class APILinksAndData(APILinks):
    data: Optional[Union[str, APIDataWithFields, APIDataBase, list[Union[str, APIDataWithFields, APIDataBase]]]] = None


class APIData(APIDataWithFields):
    fields: dict
    relationships: dict[str, Optional[Union[APILinksAndData, APILinks, list[Union[APILinksAndData, APILinks]]]]]
    links: APILinksType

    @field_validator("relationships", mode="before")
    @classmethod
    def transform_relationships(cls, v: Any):
        return dict(v)


class APIResponse(APILinks):
    data: APIData
    meta: Optional[dict] = None


class ListAPIResponse(APIResponse):
    data: list[Union[APIData, dict]]
    links: APILinksType

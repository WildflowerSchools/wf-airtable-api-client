from typing import Optional, Union

from pydantic import RootModel

from .base_model import BaseModel
from . import response as response_models

MODEL_TYPE = "auto_response_email_template"


class APIAutoResponseEmailTemplateFields(BaseModel):
    geographic_areas: Optional[list[str]] = None
    sendgrid_template_id: Optional[str] = None
    contact_type: Optional[str] = None
    language: Optional[str] = None
    first_contact_email: Optional[str] = None
    marketing_source: Optional[str] = None


class APIAutoResponseEmailTemplateRelationships(BaseModel):
    hub: Optional[response_models.APILinksAndData] = None
    assigned_rse: Optional[response_models.APILinksAndData] = None
    geographic_areas: Optional[response_models.APILinksAndData] = None


class APIAutoResponseEmailTemplateData(response_models.APIData):
    fields: APIAutoResponseEmailTemplateFields


class ListAPIAutoResponseEmailTemplateData(RootModel):
    root: list[APIAutoResponseEmailTemplateData]


class APIAutoResponseEmailTemplateResponse(response_models.APIResponse):
    data: APIAutoResponseEmailTemplateData


class ListAPIAutoResponseEmailTemplateResponse(response_models.ListAPIResponse):
    data: list[Union[APIAutoResponseEmailTemplateData, dict]]

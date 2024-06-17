from datetime import datetime
from typing import Optional

from .base_model import BaseModel
from . import response as response_models

MODEL_TYPE = "ssj_fillout_get_involved"


class CreateApiSSJFilloutGetInvolvedFields(BaseModel):
    educator_id: Optional[str] = None

    first_name: str = None
    last_name: str = None
    email: str = None

    contact_type: str = None

    is_montessori_certified: bool = False
    is_seeking_montessori_certification: bool = False
    montessori_certification_certifier_1: Optional[str] = None
    montessori_certification_year_1: Optional[int] = None
    montessori_certification_level_1: Optional[list[str]] = []
    montessori_certification_certifier_2: Optional[str] = None
    montessori_certification_year_2: Optional[int] = None
    montessori_certification_level_2: Optional[list[str]] = []
    montessori_certification_certifier_3: Optional[str] = None
    montessori_certification_year_3: Optional[int] = None
    montessori_certification_level_3: Optional[list[str]] = []
    montessori_certification_certifier_4: Optional[str] = None
    montessori_certification_year_4: Optional[int] = None
    montessori_certification_level_4: Optional[list[str]] = []

    city: str = None
    state: str = None
    country: Optional[str] = None

    age_classrooms_interested_in_offering: Optional[list[str]] = None
    educator_interests: Optional[list[str]] = None
    educator_interests_other: Optional[str] = None

    community_member_interest: Optional[str] = None
    community_member_support_finding_teachers: Optional[bool] = None
    community_member_community_info: Optional[str] = None
    community_member_self_info: Optional[str] = None

    socio_economic_race_and_ethnicity: Optional[list[str]] = []
    socio_economic_race_and_ethnicity_other: Optional[str] = None
    socio_economic_pronouns: Optional[str] = None
    socio_economic_pronouns_other: Optional[str] = None
    socio_economic_gender: Optional[str] = None
    socio_economic_gender_other: Optional[str] = None
    socio_economic_household_income: Optional[str] = None
    socio_economic_primary_language: Optional[str] = None
    socio_economic_primary_language_other: Optional[str] = None

    message: Optional[str] = None
    source: Optional[str] = None
    receive_communications: bool = False

    marketing_source: Optional[str] = None
    marketing_campaign: Optional[str] = None

    entry_date: datetime = None


class ApiSSJFilloutGetInvolvedFields(CreateApiSSJFilloutGetInvolvedFields):
    response_id: str = None
    created_at: Optional[datetime] = None


class ApiSSJFilloutGetInvolvedData(response_models.APIData):
    fields: ApiSSJFilloutGetInvolvedFields


class ApiSSJFilloutGetInvolvedResponse(response_models.APIResponse):
    data: ApiSSJFilloutGetInvolvedData

import json
import logging
from typing import Union

import requests
from requests.adapters import HTTPAdapter, Retry

from wf_airtable_api_schema.models.hubs import APIHubResponse, ListAPIHubResponse
from wf_airtable_api_schema.models.pods import APIPodResponse, ListAPIPodResponse
from wf_airtable_api_schema.models.partners import APIPartnerResponse, ListAPIPartnerResponse
from wf_airtable_api_schema.models.schools import APISchoolResponse, ListAPISchoolResponse
from wf_airtable_api_schema.models.educators import APIEducatorResponse, ListAPIEducatorResponse, \
    CreateAPIEducatorFields
from wf_airtable_api_schema.models.geo_area_contacts import APIGeoAreaContactResponse, ListAPIGeoAreaContactResponse
from wf_airtable_api_schema.models.geo_area_target_communities import APIGeoAreaTargetCommunityResponse, ListAPIGeoAreaTargetCommunityResponse
from wf_airtable_api_schema.models.ssj_typeform_start_a_school import CreateApiSSJTypeformStartASchoolFields, \
    ApiSSJTypeformStartASchoolResponse

from .. import const


logger = logging.getLogger(__name__)


class Api:
    def __init__(self,
                 audience: str = const.WF_AUTH0_AIRTABLE_API_AUDIENCE,
                 auth_domain: str = const.WF_AUTH0_DOMAIN,
                 client_id: str = const.WF_AUTH0_CLIENT_ID,
                 client_secret: str = const.WF_AUTH0_CLIENT_SECRET,
                 api_url: str = const.WF_AIRTABLE_API_URL):
        self.audience = audience
        self.auth_domain = auth_domain
        self.auth_url = f"https://{self.auth_domain}".rstrip("/")

        self.client_id = client_id
        self.client_secret = client_secret

        self.api_url = api_url.rstrip("/")
        self.session = self._init_request_retry_object()
        self.access_token = self._load_access_token()

    def _init_request_retry_object(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.2,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    def _load_access_token(self):
        response = self.session.post(
            url=f"{self.auth_url}/oauth/token",
            data=json.dumps({
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "audience": self.audience,
                "grant_type": "client_credentials"}),
            headers={"content-type": "application/json"})

        data = response.json()
        return data['access_token']

    def request(self, method, path, params: dict = None, data: Union[dict, bytes] = None):
        url = f"{self.api_url}/{path}"

        d = data
        if isinstance(data, dict):
            d = json.dumps(data).encode("utf-8")

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=d,
                headers={
                    "content-type": "application/json",
                    "authorization": f"Bearer {self.access_token}"
                }
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            logger.exception(f"Request HTTPError ({err.response.status_code}): {url}")
            raise err
        except requests.exceptions.ConnectionError as err:
            logger.exception(f"Request ConnectionError: {url}")
            raise err
        except requests.exceptions.Timeout as err:
            logger.exception(f"Request Timeout: {url}")
            raise err
        except requests.exceptions.RequestException as err:
            logger.exception(f"Unexpected RequestException ({err.response.status_code}): {url}")
            raise err

    def get(self, path, params: dict = None):
        response = self.request(
            method="GET",
            path=path,
            params=params
        )
        return response.json()

    def post(self, path, params: dict = None, data: dict = None):
        response = self.request(
            method="POST",
            path=path,
            params=params,
            data=data
        )
        return response.json()

    def list_hubs(self):
        r = self.get("hubs")
        response = ListAPIHubResponse.parse_obj(r)
        return response

    def get_hub(self, hub_id):
        r = self.get(f"hubs/{hub_id}")
        response = APIHubResponse.parse_obj(r)
        return response

    def get_hub_regional_site_entrepreneurs(self, hub_id):
        r = self.get(f"hubs/{hub_id}/regional_site_entrepreneurs")
        response = ListAPIPartnerResponse.parse_obj(r)
        return response

    def get_hub_pods(self, hub_id):
        r = self.get(f"hubs/{hub_id}/pods")
        response = ListAPIPodResponse.parse_obj(r)
        return response

    def get_hub_schools(self, hub_id):
        r = self.get(f"hubs/{hub_id}/schools")
        response = ListAPISchoolResponse.parse_obj(r)
        return response

    def list_pods(self):
        r = self.get("pods")
        response = ListAPIPodResponse.parse_obj(r)
        return response

    def get_pod(self, pod_id):
        r = self.get(f"pods/{pod_id}")
        response = APIPodResponse.parse_obj(r)
        return response

    def list_partners(self, page_size=50, offset=""):
        r = self.get("partners", {"page_size": page_size, "offset": offset})
        response = ListAPIPartnerResponse.parse_obj(r)
        return response

    def get_partner(self, partner_id):
        r = self.get(f"partners/{partner_id}")
        response = APIPartnerResponse.parse_obj(r)
        return response

    def list_schools(self, page_size=50, offset=""):
        r = self.get("schools", {"page_size": page_size, "offset": offset})
        response = ListAPISchoolResponse.parse_obj(r)
        return response

    def get_school(self, school_id):
        r = self.get(f"schools/{school_id}")
        response = APISchoolResponse.parse_obj(r)
        return response

    def list_educators(self, page_size=50, offset=""):
        r = self.get("educators", {"page_size": page_size, "offset": offset})
        response = ListAPIEducatorResponse.parse_obj(r)
        return response

    def get_educator(self, educator_id):
        r = self.get(f"educators/{educator_id}")
        response = APIEducatorResponse.parse_obj(r)
        return response

    def get_educator_by_email(self, email):
        r = self.get(f"educators/find_by_email/{email}")
        response = APIEducatorResponse.parse_obj(r)
        return response

    def create_educator(self, educator_payload: CreateAPIEducatorFields):
        r = self.post("educators", data=educator_payload.dict())
        response = APIEducatorResponse.parse_obj(r)
        return response

    def list_geo_area_contacts(self):
        r = self.get("geo_mapping/contacts")
        response = ListAPIGeoAreaContactResponse.parse_obj(r)
        return response

    def get_geo_area_contact_for_address(self, address):
        r = self.get("geo_mapping/contacts/for_address", params={"address": address})
        response = APIGeoAreaContactResponse.parse_obj(r)
        return response

    def get_geo_area_contact(self, geo_area_contact_id):
        r = self.get(f"geo_mapping/contacts/{geo_area_contact_id}")
        response = APIGeoAreaContactResponse.parse_obj(r)
        return response

    def list_geo_area_target_communities(self):
        r = self.get("geo_mapping/target_communities")
        response = ListAPIGeoAreaTargetCommunityResponse.parse_obj(r)
        return response

    def get_geo_area_target_community_for_address(self, address):
        r = self.get("geo_mapping/target_communities/for_address", params={"address": address})
        response = APIGeoAreaTargetCommunityResponse.parse_obj(r)
        return response

    def get_geo_area_target_community(self, geo_area_target_community_id):
        r = self.get(f"geo_mapping/target_communities/{geo_area_target_community_id}")
        response = APIGeoAreaTargetCommunityResponse.parse_obj(r)
        return response

    def create_survey_response(self, survey_payload: CreateApiSSJTypeformStartASchoolFields):
        r = self.post("ssj_typeforms/start_a_school_response", data=survey_payload.dict())
        response = ApiSSJTypeformStartASchoolResponse.parse_obj(r)
        return response

import json
import logging
import requests
from requests.adapters import HTTPAdapter, Retry

from wf_airtable_api_schema.models.hubs import APIHubResponse, ListAPIHubResponse
from wf_airtable_api_schema.models.pods import APIPodResponse, ListAPIPodResponse
from wf_airtable_api_schema.models.partners import APIPartnerResponse, ListAPIPartnerResponse
from wf_airtable_api_schema.models.schools import APISchoolResponse, ListAPISchoolResponse
from wf_airtable_api_schema.models.educators import APIEducatorResponse, ListAPIEducatorResponse
from wf_airtable_api_schema.models.location_contacts import APILocationContactResponse, ListAPILocationContactResponse

from .. import const


logger = logging.getLogger(__name__)

class Api:
    def __init__(self,
                 audience: str = const.WF_AIRTABLE_API_AUTH0_AUDIENCE,
                 auth_domain: str = const.WF_AIRTABLE_API_AUTH0_DOMAIN,
                 client_id: str = const.WF_AIRTABLE_API_AUTH0_CLIENT_ID,
                 client_secret: str = const.WF_AIRTABLE_API_AUTH0_CLIENT_SECRET,
                 api_url: str = const.WF_AIRTABLE_API_URL):
        self.audience = audience
        self.auth_domain = auth_domain
        self.auth_url = f"https://{self.auth_domain}".rstrip("/")

        self.client_id = client_id
        self.client_secret = client_secret

        self.api_url = api_url.rstrip("/")
        self.request = self._init_request_retry_object()
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
        response = self.request.post(
            url=f"{self.auth_url}/oauth/token",
            data=json.dumps({
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "audience": self.audience,
                "grant_type": "client_credentials"}),
            headers={"content-type": "application/json"})

        data = response.json()
        return data['access_token']

    def get(self, path, params: dict = None):
        try:
            url = f"{self.api_url}/{path}"

            response = self.request.get(
                url=url,
                params=params,
                headers={
                    "content-type": "application/json",
                    "authorization": f"Bearer {self.access_token}"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            logger.exception(f"Unexpected RequestException ({err.response.status_code}): {url}")
            raise(err)
        except requests.exceptions.HTTPError as err:
            logger.exception(f"Request HTTPError ({err.response.status_code}): {url}")
            raise(err)
        except requests.exceptions.ConnectionError as err:
            logger.exception(f"Request ConnectionError: {url}")
            raise(err)
        except requests.exceptions.Timeout as err:
            logger.exception(f"Request Timeout: {url}")
            raise(err)

    def list_hubs(self):
        h = self.get("hubs")
        response = ListAPIHubResponse.parse_obj(h)
        return response

    def get_hub(self, hub_id):
        h = self.get(f"hubs/{hub_id}")
        response = APIHubResponse.parse_obj(h)
        return response

    def get_hub_regional_site_entrepreneurs(self, hub_id):
        h = self.get(f"hubs/{hub_id}/regional_site_entrepreneurs")
        response = ListAPIPartnerResponse.parse_obj(h)
        return response

    def get_hub_pods(self, hub_id):
        h = self.get(f"hubs/{hub_id}/pods")
        response = ListAPIPodResponse.parse_obj(h)
        return response

    def get_hub_schools(self, hub_id):
        h = self.get(f"hubs/{hub_id}/schools")
        response = ListAPISchoolResponse.parse_obj(h)
        return response

    def list_pods(self):
        h = self.get("pods")
        response = ListAPIPodResponse.parse_obj(h)
        return response

    def get_pod(self, pod_id):
        h = self.get(f"pods/{pod_id}")
        response = APIPodResponse.parse_obj(h)
        return response

    def list_partners(self):
        h = self.get("partners")
        response = ListAPIPartnerResponse.parse_obj(h)
        return response

    def get_partner(self, partner_id):
        h = self.get(f"partners/{partner_id}")
        response = APIPartnerResponse.parse_obj(h)
        return response

    def list_schools(self):
        h = self.get("schools")
        response = ListAPISchoolResponse.parse_obj(h)
        return response

    def get_school(self, school_id):
        h = self.get(f"schools/{school_id}")
        response = APISchoolResponse.parse_obj(h)
        return response

    def list_educators(self):
        h = self.get("educators")
        response = ListAPIEducatorResponse.parse_obj(h)
        return response

    def get_educator(self, educator_id):
        h = self.get(f"educators/{educator_id}")
        response = APIEducatorResponse.parse_obj(h)
        return response

    def list_location_contacts(self):
        h = self.get("location_contacts")
        response = ListAPILocationContactResponse.parse_obj(h)
        return response

    def get_location_contact_for_address(self, address):
        h = self.get("location_contacts/contact_for_address", params={"address": address})
        response = APILocationContactResponse.parse_obj(h)
        return response

    def get_location_contact(self, educator_id):
        h = self.get(f"location_contacts/{educator_id}")
        response = APILocationContactResponse.parse_obj(h)
        return response

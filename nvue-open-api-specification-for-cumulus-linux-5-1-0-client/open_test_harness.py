from unittest import TestCase

import respx

from nvue_open_api_specification_for_cumulus_linux_5_1_0_client import Client
from nvue_open_api_specification_for_cumulus_linux_5_1_0_client.api.interface import get_interface

#  openapi-python-client generate --path openapi.json

class OpenAPITest(TestCase):

    @respx.mock(base_url='http://localhost:8450')
    def test_nvue_api(self, respx_mock):
        client = Client(base_url="http://localhost:8450/", timeout=10, verify_ssl=True)
        response = get_interface.sync_detailed(client=client)

        self.assertEqual(200, response.status_code)

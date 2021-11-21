import os
from typing import Dict, Any

from pycti.connector_v2.connectors.connector import ApplicationSettings
from pycti.connector_v2.connectors.external_import_connector import (
    ExternalImportConnector,
)
from pycti.connector_v2.connectors.import_file_connector import (
    InternalImportFileConnector,
)
from pycti.connector_v2.libs.mixins.http import HttpMixin


class EIModel(ApplicationSettings):
    url: str


class ExternalImportConnectorv2(ExternalImportConnector, HttpMixin):
    def __init__(self):
        super().__init__(EIModel)

    def test_setup(self, api_client):
        os.environ[
            "APP_URL"
        ] = "https://github.com/oasis-open/cti-stix-common-objects/raw/main/objects/marking-definition/marking-definition--62fd3f9b-15f3-4ebc-802c-91fce9536bcf.json"

    def test_teardown(self, api_client):
        api_client.marking_definition.delete(
            id="marking-definition--62fd3f9b-15f3-4ebc-802c-91fce9536bcf"
        )

    def _run(self):
        self.logger.info(self.config.app.url)
        url = self.config.app.url
        content = self.get(url)

        # send data
        self.send_stix2_bundle(bundle=content, update=True)


class TestExternalImportConnectors:
    @staticmethod
    def case_external_import_connector_v2():
        return ExternalImportConnectorv2


class ImportReportFileConnectorv2(InternalImportFileConnector):
    def __init__(self):
        super().__init__(ApplicationSettings)

    def test_setup(self, api_client):
        api_client.upload_file(
            file_name="./tests/e2e/support_data/test_location.json",
        )

    def test_teardown(self, api_client):
        api_client.stix_domain_object.delete(
            id="location--011a9d8e-75eb-475a-a861-6998e9968287"
        )

    def _run(self, data: Dict) -> str:
        file_content = self._download_import_file(data)

        # send data
        self.send_stix2_bundle(file_content)

        return "Finished"

    def _download_import_file(self, data: Dict) -> Any:
        file_fetch = data["file_fetch"]
        file_uri = self.get_opencti_url() + file_fetch
        # file_name = os.path.basename(file_fetch)
        file_content = self.api.fetch_opencti_file(file_uri, True)

        return file_content


class TestInternalImportFileConnectors:
    @staticmethod
    def case_internal_file_import_connector_v2():
        return ImportReportFileConnectorv2

import unittest

from apps.scan_engine_api.models import SearchEngine
from tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    def setUp(self):
        self.acunetix_api = SearchEngine()
        self.target_url = 'http://rusudanabuselize86.blogspot.com/'
        self.target_url_description = 'Portfolio website'

    def test_get_scans(self):
        scan_id = '771fc67d-9892-40fd-81a6-9f75bdfa227d'
        report_id, status = self.acunetix_api.register_report(scan_id)
        self.assertIsNotNone(report_id)

    def test_get_report_meta(self):
        scan_id = '771fc67d-9892-40fd-81a6-9f75bdfa227d'
        report_id, status = self.acunetix_api.register_report(scan_id)
        self.assertIsNotNone(report_id)
        response, status = self.acunetix_api.report_meta(report_id)
        print(response)
        self.assertIsNotNone(response)

    def test_download_report(self):
        file_path = '42567e2b64c9e3281ad64a1ce8b0bc2d3d4c96ed907ebec5a0a5c79a64e6779f77afda255f9ad887b4f20f49-058f-49ba-a6b0-d635ced1bb30.xml'
        response, status = self.acunetix_api.download_report(file_path)
        self.assertTrue(status)


if __name__ == '__main__':
    unittest.main()

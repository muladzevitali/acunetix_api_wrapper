import unittest

from apps.scan_engine_api.models import SearchEngine
from tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    def setUp(self):
        self.acunetix_api = SearchEngine()
        self.target_url = 'http://rusudanabuselize86.blogspot.com/'
        self.target_url_description = 'Portfolio website'

    def test_get_scans(self):
        scans, status = self.acunetix_api.scans()
        self.assertIsInstance(scans, list)

    def test_add_target(self):
        target, status = self.acunetix_api.add_target(self.target_url, self.target_url_description, criticality='low')
        self.assertIsNotNone(target.get('target_id'))

    def test_targets(self):
        targets, status = self.acunetix_api.targets(offset=109)
        self.assertIsInstance(targets, list)

    def test_add_scan(self):
        target, status = self.acunetix_api.add_target(self.target_url, self.target_url_description, criticality='low')
        target_id = target.get('target_id')
        self.assertIsNotNone(target_id)
        # scan, status = self.scan_engine_api.add_scan(target_id, profile='full_scan', schedule=False)
        # self.assertIsNotNone(scan.get('scan_id'))

    def test_get_scan_result_id(self):
        results, status = self.acunetix_api.scan_result_meta('771fc67d-9892-40fd-81a6-9f75bdfa227d')
        self.assertIsNotNone(results)

    def test_scan_vulnerabilities(self):
        scan_id = '47f8dd84-94a7-4c34-8623-9964461eeac4'
        results, _ = self.acunetix_api.scan_result_meta(scan_id)
        if not results:
            return

        result_ids = [result.get('result_id') for result in results]
        vulnerabilities = list()
        for result_id in result_ids:
            result_vulnerabilities, status = self.acunetix_api.scan_result_vulnerabilities(scan_id, result_id)
            if not status:
                continue
            vulnerabilities.extend(result_vulnerabilities)

        self.assertIsInstance(vulnerabilities, list)

    def test_vulnerability_detail(self):
        scan_id = '771fc67d-9892-40fd-81a6-9f75bdfa227d'
        result_id = 'd66d07a9-ffe7-4c4e-adc0-9858f65de426'
        vulnerability_id = '011055fc-94f1-ab96-56ac-53117c56fb4d'

        vulnerability_detail, status = self.acunetix_api.scan_vulnerability_detail(scan_id, result_id, vulnerability_id)
        self.assertIsInstance(vulnerability_detail, dict)
        self.assertIs(status, True)

    def test_vulnerability_types(self):
        scan_id = '771fc67d-9892-40fd-81a6-9f75bdfa227d'
        result_id = 'd66d07a9-ffe7-4c4e-adc0-9858f65de426'

        vulnerability_types, status = self.acunetix_api.scan_vulnerability_types(scan_id, result_id)
        self.assertIsInstance(vulnerability_types, list)
        self.assertIs(status, True)

    def test_pause_scan(self):
        target_id = '7a04c4a2-aac4-4c50-a1b1-a52eee0928ab'
        scan, status = self.acunetix_api.add_scan(target_id, profile='full_scan', schedule=False)
        self.assertIsNotNone(scan.get('scan_id'))
        scan_id = scan.get('scan_id')
        status = self.acunetix_api.pause_scan(scan_id)


if __name__ == '__main__':
    unittest.main()

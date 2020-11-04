from .base import SearchEngineBaseApi


class Result(SearchEngineBaseApi):
    def scan_result_meta(self, scan_id: str):
        """
        Get scan result meta such as result_id, start date, end_date and status
        """
        endpoint = 'scans/%s/results' % scan_id
        response, status = self.get(endpoint)
        response_json = response.json()
        results = response_json.get('results', [])

        if not results:
            return list(), False
        return results, status

    def scan_result_vulnerabilities(self, scan_id: str, result_id: str, limit: int = 100, offset: int = 0):
        """
        Get vulnerabilities of given result id of a scan
        """
        endpoint = 'scans/%s/results/%s/vulnerabilities' % (scan_id, result_id)
        vulnerabilities = list()
        while True:
            params = (('l', limit), ('c', offset),)

            response, status = self.get(endpoint, params=params)
            response_json = response.json()
            current_vulnerabilities = response_json.get('vulnerabilities', [])

            if not current_vulnerabilities or not status:
                break

            vulnerabilities.extend(current_vulnerabilities)
            offset += limit

        return vulnerabilities, status

    def scan_vulnerability_detail(self, scan_id: str, result_id: str, vulnerability_id: str):
        """
        Get details of a given vulnerability
        """
        endpoint = 'scans/%s/results/%s/vulnerabilities/%s' % (scan_id, result_id, vulnerability_id)
        response, status = self.get(endpoint)
        response_json = response.json()

        return response_json, status

    def scan_vulnerability_types(self, scan_id: str, result_id: str, limit: int = 100, offset: int = 0):
        """
        Get vulnerability types for a given result of scan
        """
        endpoint = 'scans/%s/results/%s/vulnerability_types' % (scan_id, result_id)
        vulnerability_types = list()
        while True:
            params = (('l', limit), ('c', offset),)

            response, status = self.get(endpoint, params=params)
            response_json = response.json()
            current_types = response_json.get('vulnerability_types', [])

            if not current_types or not status:
                break

            vulnerability_types.extend(current_types)
            offset += limit

        return vulnerability_types, status

    def result_statistics(self, scan_id: str, result_id: str):
        """Get Result statistics for given scan"""
        endpoint = 'scans/%s/results/%s/statistics' % (scan_id, result_id)
        response, status = self.get(endpoint)
        response_json = response.json()

        return response_json, status

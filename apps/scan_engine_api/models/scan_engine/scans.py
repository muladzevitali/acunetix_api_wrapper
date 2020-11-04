from .base import SearchEngineBaseApi

scan_profiles = {
    'full_scan': '11111111-1111-1111-1111-111111111111',
    'high_risk_vulnerabilities': '11111111-1111-1111-1111-111111111112',
    'cross_site_scripting_vulnerabilities': '11111111-1111-1111-1111-111111111116',
    'sql_injection_vulnerabilities': '11111111-1111-1111-1111-111111111113',
    'weak_passwords': '11111111-1111-1111-1111-111111111115',
    'crawl_only': '11111111-1111-1111-1111-111111111117'
}


class Scan(SearchEngineBaseApi):

    def scans(self, limit: int = 100, offset: int = 0):
        """
        Get all the scans
        :param limit: limit per fetch
        :param offset: start point for current fetch
        """
        endpoint = 'scans'
        scans = list()
        while True:
            params = (('l', limit), ('c', offset),)

            response, status = self.get(endpoint, params=params)
            response_json = response.json()
            current_scans = response_json.get('scans', [])
            if not current_scans or not status:
                break
            scans.extend(current_scans)
            offset += limit

        return scans, True

    def get_scan(self, scan_id: str):
        """
        Get information from scan
        """
        endpoint = 'scans/{scan_id}'.format(scan_id=scan_id)
        response, status = self.get(endpoint)
        response_json = response.json()

        return response_json, status

    def add_scan(self, target_id: str, profile: str = 'full_scan', schedule: bool = False):
        """
        Add scan
        :param target_id: id of target website
        :param profile: must be one of ('full_scan', 'high_risk_vulnerabilities', 'cross_site_scripting_vulnerabilities',
                        'sql_injection_vulnerabilities', 'weak_passwords', 'crawl_only')
        :param schedule:
        """

        endpoint = 'scans'
        profile_id = scan_profiles.get(profile)
        if not profile:
            return list(), False

        scheduler = dict(disable=not schedule)
        data = dict(target_id=target_id, profile_id=profile_id, schedule=scheduler)

        response, status = self.post(endpoint, json=data)
        if not status:
            return response, status

        response_json = response.json()
        scan_id = response.headers.get('Location', '').split('/')[-1]

        return {**response_json, 'scan_id': scan_id}, status

    def pause_scan(self, scan_id: str):
        """Pause scan"""
        endpoint = 'scans/%s/pause' % scan_id
        response, status = self.post(endpoint)

        return status

    def resume_scan(self, scan_id: str):
        """Resume paused scan"""
        endpoint = 'scans/%s/resume' % scan_id
        response, status = self.post(endpoint)

        return status

    def abort_scan(self, scan_id: str):
        """Abort scan"""
        endpoint = 'scans/%s/abort' % scan_id
        response, status = self.post(endpoint)

        return status

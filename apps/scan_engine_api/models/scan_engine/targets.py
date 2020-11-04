from .base import SearchEngineBaseApi

target_criticality = dict(critical=30, high=20, normal=10, low=0)
login_kinds = ['none', 'automatic', 'sequence']
scan_speeds = ['fast', 'moderate', 'slow', 'sequential']


class Target(SearchEngineBaseApi):

    def targets(self, limit: int = 100, offset: int = 0, s: str = ''):
        """
        Get all the scans
        :param limit: limit per fetch
        :param offset: start point for current fetch
        :param s: string
        :return:
        """
        endpoint = 'targets'
        targets = list()
        while True:
            params = (('l', limit), ('c', offset), ('s', s),)

            response, status = self.get(endpoint, params=params)
            response_json = response.json()
            current_targets = response_json.get('targets', [])

            if not current_targets or not status:
                break

            targets.extend(current_targets)
            offset += limit

        return targets, status

    def add_target(self, url_address: str, description: str = '', type: str = 'default', criticality: str = 'normal'):
        """
        Api wrapper for add target
        :param url_address: url address of website
        :param description: description length must be less than 1024
        :param type: must be one of (default, demo, network)
        :param criticality: must be one of (30, 20, 10, 0) meaning (Critical, High, Normal, Low)
        :return:
        """
        endpoint = 'targets'
        criticality = target_criticality.get(criticality, -1)
        if criticality < 0:
            return dict(), False

        data = dict(address=url_address, description=description, type=type, criticality=criticality)
        response, status = self.post(endpoint, json=data)
        response_json = response.json()

        return response_json, status

    @staticmethod
    def form_login_config(login_meta: dict):
        """
        Check and form login config for target edit
        """
        login_params = ['kind', 'username', 'password']
        if not any(login_meta.get(param) for param in login_params):
            return dict(), False

        kind = login_meta.get('kind', 'automatic')
        username = login_meta.get('username')
        password = login_meta.get('password')
        login_data = {
            "kind": kind,
            "credentials": {
                "enabled": True,
                "username": username,
                "password": password
            }}

        return login_data, True

    @staticmethod
    def form_authentication(authentication_meta: dict):
        """
        Check and form authentication config for target update
        """
        authentication_params = ['username', 'password']
        if not any(authentication_meta.get(param) for param in authentication_params):
            return dict(), False

        authentication_meta['enabled'] = True

        return authentication_meta, True

    def edit_target(self, target_id: str, target_url, **kwargs):
        """Edit target, add authentication/authorization etc..."""
        endpoint = 'targets/%s/configuration' % target_id
        data = dict()

        login_data, status = self.form_login_config(kwargs.get('login', {}))
        if status:
            data['login'] = login_data

        authentication_data, status = self.form_authentication(kwargs.get('authentication', {}))
        if status:
            data['authentication'] = authentication_data

        if kwargs.get('user_agent'):
            data['user_agent'] = kwargs.get('user_agent')

        if kwargs.get('custom_headers') and isinstance(kwargs.get('custom_headers'), list):
            data['custom_headers'] = kwargs.get('custom_headers')

        if kwargs.get('custom_cookies') and isinstance(kwargs.get('custom_cookies'), list):
            data['custom_cookies'] = kwargs.get('custom_cookies')

        if kwargs.get('scan_speed') and kwargs.get('scan_speed') in scan_speeds:
            data['scan_speed'] = kwargs.get('scan_speed')
        response, status = self.patch(endpoint, json=data)

        return response, status

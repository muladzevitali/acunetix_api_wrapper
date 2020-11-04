from flask_restful import (Resource)

from apps.auth import auth_required
from ..models import (SearchEngine)


class ResultMeta(Resource):
    """Class for """
    method_decorators = [auth_required]

    def get(self, scan_id):
        api_client = SearchEngine()
        results, status = api_client.scan_result_meta(scan_id)
        if not status:
            return {'message': 'scan not found with given id'}, 404

        return results, 200


class Vulnerabilities(Resource):
    method_decorators = [auth_required]

    def get(self, scan_id):
        api_client = SearchEngine()
        results, status = api_client.scan_result_meta(scan_id)
        if not status:
            return {'message': 'no results for given scan'}, 404
        if not results:
            return {'vulnerabilities': []}, 200

        result_ids = [result.get('result_id') for result in results]
        vulnerabilities = list()
        for result_id in result_ids:
            result_vulnerabilities, status = api_client.scan_result_vulnerabilities(scan_id, result_id)
            if not status:
                continue

            vulnerabilities.extend(result_vulnerabilities)

        return {'vulnerabilities': vulnerabilities}, 200


class ScanStatistics(Resource):
    method_decorators = [auth_required]

    def get(self, scan_id):
        api_client = SearchEngine()
        results, status = api_client.scan_result_meta(scan_id)
        if not status:
            return {'message': 'no results for given scan'}, 404
        if not results:
            return {'vulnerabilities': 'no results for given scan_id'}, 200

        result_ids = [result.get('result_id') for result in results]

        results_statistics, status = api_client.result_statistics(scan_id, result_ids[0])

        return {'statistics': results_statistics}, 200

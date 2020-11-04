from io import BytesIO
from pathlib import Path

from .base import SearchEngineBaseApi


class Report(SearchEngineBaseApi):
    def register_report(self, scan_id: str):
        """Register xml report"""
        endpoint = 'reports'
        data = {"template_id": "21111111-1111-1111-1111-111111111111",
                "source": {"list_type": "scans", "id_list": [scan_id]}}

        response, status = self.post(endpoint, json=data)
        if not status:
            return '', False

        report_id = response.headers.get('Location', '').split('/')[-1]

        return report_id, status

    def report_meta(self, report_id: str):
        """Get report meta. Mostly use for report status"""
        endpoint = 'reports/%s' % report_id
        response, status = self.get(endpoint)
        response_json = response.json()

        if not status:
            return response_json, False

        if not response_json.get('download'):
            response_json.pop('download')

            return response_json, status

        file_path = Path(response_json.get('download', [''])[0])
        file_name = file_path.name
        response_json['download'] = file_name

        return response_json, status

    def download_report(self, file_path):
        """Download report"""
        endpoint = 'reports/download/%s' % file_path
        response, status = self.get(endpoint)
        if not status:
            response_json = response.json()
            return response_json, status

        data_stream = BytesIO()
        data_stream.write(response.content)
        data_stream.seek(0)

        return data_stream, status

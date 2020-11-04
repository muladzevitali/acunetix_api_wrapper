from flask import send_file
from flask_restful import (Resource, reqparse)

from apps.auth import auth_required
from ..models import (SearchEngine)

parser = reqparse.RequestParser()
parser.add_argument('scan_id', type=str, required=True)


class RegisterReport(Resource):
    """Class for generating report"""
    method_decorators = [auth_required]

    def post(self):
        api_client = SearchEngine()
        args = parser.parse_args()
        report_id, status = api_client.register_report(args.get('scan_id'))
        if not status:
            return {'message': 'scan not found with given id'}, 404

        return {'report_id': report_id}, 200


class GetReport(Resource):
    """Class for getting report status and metadata"""
    method_decorators = [auth_required]

    def get(self, report_id):
        api_client = SearchEngine()
        results, status = api_client.report_meta(report_id)
        status = 200 if status else 400

        return results, status


class DownloadReport(Resource):
    method_decorators = [auth_required]

    def get(self, file_name):
        api_client = SearchEngine()
        file_or_error, status = api_client.download_report(file_name)
        if not status:
            return file_or_error, 400

        return send_file(file_or_error, attachment_filename=file_name)

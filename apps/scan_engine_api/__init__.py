from flask import Blueprint
from flask_restful import Api

from .resources import (Scan, ResultMeta, Vulnerabilities, ScanStatistics, AbortScan, ResumeScan, PauseScan,
                        GetReport, DownloadReport, RegisterReport)

search_engine_app = Blueprint(__name__, 'search_engine_app')
search_engine_api = Api(search_engine_app)

search_engine_api.add_resource(Scan, '/scans', '/scans/<scan_id>')
search_engine_api.add_resource(AbortScan, '/scans/<scan_id>/abort')
search_engine_api.add_resource(ResumeScan, '/scans/<scan_id>/resume')
search_engine_api.add_resource(PauseScan, '/scans/<scan_id>/pause')
search_engine_api.add_resource(ResultMeta, '/scans/<scan_id>/results')
search_engine_api.add_resource(Vulnerabilities, '/scans/<scan_id>/vulnerabilities')
search_engine_api.add_resource(ScanStatistics, '/scans/<scan_id>/statistics')
search_engine_api.add_resource(RegisterReport, '/reports')
search_engine_api.add_resource(GetReport, '/reports/<report_id>')
search_engine_api.add_resource(DownloadReport, '/reports/download/<file_name>')

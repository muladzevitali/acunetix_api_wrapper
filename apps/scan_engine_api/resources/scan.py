from flask_restful import (Resource, reqparse, inputs)

from apps.auth import auth_required
from ..models import (target_criticality, scan_profiles, SearchEngine, scan_speeds)

parser = reqparse.RequestParser()
parser.add_argument('address', type=str, required=False)
parser.add_argument('description', type=str, default='')
parser.add_argument('target_type', type=str, choices=['default', 'demo', 'network'], default='default')
parser.add_argument('target_criticality', type=str, choices=target_criticality.keys(), default='normal')
parser.add_argument('profile', type=str, choices=scan_profiles.keys(), default='full_scan')
parser.add_argument('schedule', type=inputs.boolean, default=False)
parser.add_argument('authentication', type=dict, required=False)
parser.add_argument('login', type=dict, required=False)
parser.add_argument('user_agent', type=str, required=False)
parser.add_argument('custom_headers', type=str, action='append', required=False)
parser.add_argument('custom_cookies', type=dict, action='append', required=False)
parser.add_argument('scan_speed', type=str, choices=scan_speeds, default='fast')

target_meta_params = ['authentication', 'login', 'user_agent', 'custom_headers', 'custom_cookies',
                      'scan_speed']


class Scan(Resource):
    method_decorators = [auth_required]

    def get(self, scan_id):
        api_client = SearchEngine()
        scan, status = api_client.get_scan(scan_id)

        return scan, 200

    def post(self):
        args = parser.parse_args()
        api_client = SearchEngine()
        target, status = api_client.add_target(args['address'], description=args['description'],
                                               type=args['target_type'], criticality=args['target_criticality'])

        if not target.get('target_id'):
            return {'message': target.get('message'), 'details': target.get('details')}, 400

        if any(args.get(param) for param in target_meta_params):
            target_meta = {param: args.get(param) for param in target_meta_params if args.get(param)}
            response, status = api_client.edit_target(target.get('target_id'), args.get('address'), **target_meta)

            if not status:
                return response.json(), 400

        scan, status = api_client.add_scan(target.get('target_id'), profile=args['profile'], schedule=args['schedule'])

        return scan, 200


class PauseScan(Resource):
    method_decorators = [auth_required]

    def get(self, scan_id):
        api_client = SearchEngine()
        status = api_client.pause_scan(scan_id)
        if status:
            return {'message': 'scan paused', 'scan_id': scan_id}, 201

        return {'message': "Invalid scan status", 'scan_id': scan_id}, 400


class ResumeScan(Resource):
    method_decorators = [auth_required]

    def get(self, scan_id):
        api_client = SearchEngine()
        status = api_client.resume_scan(scan_id)
        if status:
            return {'message': 'scan resumed', 'scan_id': scan_id}, 201

        return {'message': "Invalid scan status", 'scan_id': scan_id}, 400


class AbortScan(Resource):
    method_decorators = [auth_required]

    def get(self, scan_id):
        api_client = SearchEngine()
        status = api_client.abort_scan(scan_id)
        if status:
            return {'message': 'scan aborted', 'scan_id': scan_id}, 201

        return {'message': "Invalid scan status", 'scan_id': scan_id}, 400

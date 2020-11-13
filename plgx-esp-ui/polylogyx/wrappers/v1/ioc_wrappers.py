from flask_restplus import fields
from polylogyx.blueprints.v1.external_api import api


ioc_wrapper = api.model('ioc_wrapper', {
    'type': fields.String(default=None),
    'intel_type': fields.String(default=None),
    'value': fields.String(default=None),
    'threat_name': fields.String(default=None),
    'severity': fields.String(default=None),
    'created_at': fields.DateTime(default=None),
})
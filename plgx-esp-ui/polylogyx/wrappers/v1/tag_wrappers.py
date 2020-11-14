from flask_restplus import fields
from polylogyx.blueprints.v1.external_api import api

tag_name_wrapper = api.model('tag_name_wrapper', {
    'id': fields.Integer(),
    'value': fields.String(),
})

tag_wrapper = api.model('tags_list', {
    'value' : fields.Raw(),
    'nodes' : fields.Raw(),
    'packs' : fields.Raw(),
    'queries' : fields.Raw(),
    'file_paths' : fields.Raw(),
})



from pyramid.view import notfound_view_config
from pyramid.httpexceptions import HTTPNotFound


@notfound_view_config(renderer='json')
def notfound_view(request):
    """Handler global ketika rute atau entitas tidak ditemukan (HTTP 404)"""
    request.response.status = 404
    return {
        'error': 'Not Found',
        'message': 'Resource yang diminta tidak ditemukan pada server ini'
    }

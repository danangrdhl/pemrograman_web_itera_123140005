from pyramid.view import view_config


@view_config(route_name='home', renderer='json')
def my_view(request):
    """Endpoint root API yang memberikan informasi status service"""
    return {
        'project': 'pyramid_mahasiswa',
        'status': 'online',
        'author': 'Danang Ridho Laksono (123140005)',
        'endpoints': {
            'mahasiswa': '/api/mahasiswa',
            'matakuliah': '/api/matakuliah'
        }
    }

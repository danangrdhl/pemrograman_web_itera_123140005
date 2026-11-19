from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPBadRequest,
)
from ..models import Matakuliah


# 1. READ ALL: Menampilkan daftar seluruh mata kuliah
@view_config(route_name='matakuliah_list', renderer='json')
def matakuliah_list(request):
    """View untuk mengambil semua data mata kuliah"""
    dbsession = request.dbsession
    matakuliahs = dbsession.query(Matakuliah).order_by(Matakuliah.id.asc()).all()
    return {'matakuliahs': [m.to_dict() for m in matakuliahs]}


# 2. READ ONE: Menampilkan detail satu mata kuliah berdasarkan ID
@view_config(route_name='matakuliah_detail', renderer='json')
def matakuliah_detail(request):
    """View untuk melihat detail satu mata kuliah berdasarkan ID di URL"""
    dbsession = request.dbsession
    mk_id = request.matchdict['id']
    try:
        mk_id_int = int(mk_id)
    except ValueError:
        return HTTPNotFound(json_body={'error': f'Mata kuliah dengan ID {mk_id} tidak valid'})

    matakuliah = dbsession.query(Matakuliah).filter_by(id=mk_id_int).first()
    if matakuliah is None:
        return HTTPNotFound(json_body={'error': f'Mata kuliah dengan ID {mk_id} tidak ditemukan'})

    return {'matakuliah': matakuliah.to_dict()}


# 3. CREATE: Menambahkan data mata kuliah baru
@view_config(route_name='matakuliah_add', request_method='POST', renderer='json')
def matakuliah_add(request):
    """View untuk menambahkan mata kuliah baru dari payload JSON"""
    try:
        json_data = request.json_body
    except Exception:
        return HTTPBadRequest(json_body={'error': 'Payload JSON tidak valid atau kosong!'})

    # Validasi kelengkapan field wajib
    required_fields = ['kode_mk', 'nama_mk', 'sks', 'semester']
    for field in required_fields:
        if field not in json_data or json_data[field] is None:
            return HTTPBadRequest(json_body={'error': f'Field {field} wajib diisi!'})
        if isinstance(json_data[field], str) and not json_data[field].strip():
            return HTTPBadRequest(json_body={'error': f'Field {field} wajib diisi!'})

    # Validasi dan konversi sks (harus integer dan bernilai > 0)
    try:
        sks = int(json_data['sks'])
        if sks <= 0:
            return HTTPBadRequest(json_body={'error': 'Kolom sks harus bertipe integer dan bernilai lebih dari 0!'})
    except (ValueError, TypeError):
        return HTTPBadRequest(json_body={'error': 'Kolom sks harus berupa angka integer!'})

    # Validasi dan konversi semester (harus integer dan bernilai > 0)
    try:
        semester = int(json_data['semester'])
        if semester <= 0:
            return HTTPBadRequest(json_body={'error': 'Kolom semester harus bertipe integer dan bernilai lebih dari 0!'})
    except (ValueError, TypeError):
        return HTTPBadRequest(json_body={'error': 'Kolom semester harus berupa angka integer!'})

    dbsession = request.dbsession
    kode_mk = str(json_data['kode_mk']).strip().upper()

    # Validasi duplikasi kode_mk
    existing = dbsession.query(Matakuliah).filter_by(kode_mk=kode_mk).first()
    if existing:
        return HTTPBadRequest(json_body={'error': f'Mata kuliah dengan kode {kode_mk} sudah terdaftar!'})

    try:
        matakuliah = Matakuliah(
            kode_mk=kode_mk,
            nama_mk=str(json_data['nama_mk']).strip(),
            sks=sks,
            semester=semester
        )

        dbsession.add(matakuliah)
        # Flush session untuk mengeksekusi query INSERT dan mendapatkan ID primary key autoincrement
        dbsession.flush()

        return {'success': True, 'matakuliah': matakuliah.to_dict()}

    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})


# 4. UPDATE: Memperbarui data mata kuliah yang sudah ada
@view_config(route_name='matakuliah_update', request_method='PUT', renderer='json')
def matakuliah_update(request):
    """View untuk mengupdate data mata kuliah berdasarkan ID"""
    dbsession = request.dbsession
    mk_id = request.matchdict['id']
    try:
        mk_id_int = int(mk_id)
    except ValueError:
        return HTTPNotFound(json_body={'error': f'Mata kuliah dengan ID {mk_id} tidak valid'})

    matakuliah = dbsession.query(Matakuliah).filter_by(id=mk_id_int).first()
    if matakuliah is None:
        return HTTPNotFound(json_body={'error': f'Mata kuliah dengan ID {mk_id} tidak ditemukan'})

    try:
        json_data = request.json_body
    except Exception:
        return HTTPBadRequest(json_body={'error': 'Payload JSON tidak valid atau kosong!'})

    try:
        if 'kode_mk' in json_data:
            new_kode = str(json_data['kode_mk']).strip().upper()
            if not new_kode:
                return HTTPBadRequest(json_body={'error': 'Field kode_mk tidak boleh kosong!'})
            conflict = dbsession.query(Matakuliah).filter(
                Matakuliah.kode_mk == new_kode,
                Matakuliah.id != mk_id_int
            ).first()
            if conflict:
                return HTTPBadRequest(json_body={'error': f'Mata kuliah dengan kode {new_kode} sudah digunakan!'})
            matakuliah.kode_mk = new_kode

        if 'nama_mk' in json_data:
            new_nama = str(json_data['nama_mk']).strip()
            if not new_nama:
                return HTTPBadRequest(json_body={'error': 'Field nama_mk tidak boleh kosong!'})
            matakuliah.nama_mk = new_nama

        if 'sks' in json_data:
            try:
                sks = int(json_data['sks'])
                if sks <= 0:
                    return HTTPBadRequest(json_body={'error': 'Kolom sks harus bertipe integer dan bernilai lebih dari 0!'})
                matakuliah.sks = sks
            except (ValueError, TypeError):
                return HTTPBadRequest(json_body={'error': 'Kolom sks harus berupa angka integer!'})

        if 'semester' in json_data:
            try:
                semester = int(json_data['semester'])
                if semester <= 0:
                    return HTTPBadRequest(json_body={'error': 'Kolom semester harus bertipe integer dan bernilai lebih dari 0!'})
                matakuliah.semester = semester
            except (ValueError, TypeError):
                return HTTPBadRequest(json_body={'error': 'Kolom semester harus berupa angka integer!'})

        return {'success': True, 'matakuliah': matakuliah.to_dict()}

    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})


# 5. DELETE: Menghapus data mata kuliah
@view_config(route_name='matakuliah_delete', request_method='DELETE', renderer='json')
def matakuliah_delete(request):
    """View untuk menghapus mata kuliah berdasarkan ID"""
    dbsession = request.dbsession
    mk_id = request.matchdict['id']
    try:
        mk_id_int = int(mk_id)
    except ValueError:
        return HTTPNotFound(json_body={'error': f'Mata kuliah dengan ID {mk_id} tidak valid'})

    matakuliah = dbsession.query(Matakuliah).filter_by(id=mk_id_int).first()
    if matakuliah is None:
        return HTTPNotFound(json_body={'error': f'Mata kuliah dengan ID {mk_id} tidak ditemukan'})

    dbsession.delete(matakuliah)

    return {'success': True, 'message': f'Mata kuliah dengan ID {mk_id} berhasil dihapus'}

import os
import unittest
from pyramid import testing
from webtest import TestApp
from pyramid_mahasiswa import main
from pyramid_mahasiswa.scripts.initialize_db import setup_models
from pyramid_mahasiswa.models import Base, get_engine, get_session_factory, get_tm_session
import transaction

TEST_DB_FILE = 'test_api.sqlite'
TEST_DB_URL = f'sqlite:///{TEST_DB_FILE}'


class TestMahasiswaMatakuliahAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Bersihkan file db test lama jika ada
        if os.path.exists(TEST_DB_FILE):
            try:
                os.remove(TEST_DB_FILE)
            except OSError:
                pass

        cls.settings = {
            'sqlalchemy.url': TEST_DB_URL,
            'pyramid.includes': ['pyramid_jinja2', 'pyramid_tm'],
            'tm.manager_hook': 'pyramid_tm.explicit_manager',
        }
        app = main({}, **cls.settings)
        cls.testapp = TestApp(app)

        # Inisialisasi tabel dan seeding awal
        cls.engine = get_engine(cls.settings)
        Base.metadata.create_all(bind=cls.engine)

        session_factory = get_session_factory(cls.engine)
        cls.dbsession = get_tm_session(session_factory, transaction.manager)

        with transaction.manager:
            setup_models(cls.dbsession)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
        if os.path.exists(TEST_DB_FILE):
            try:
                os.remove(TEST_DB_FILE)
            except OSError:
                pass

    def tearDown(self):
        testing.tearDown()

    # ==========================================
    # PENGUJIAN ROOT & MAHASISWA API
    # ==========================================

    def test_01_root_home(self):
        """Uji endpoint root GET /"""
        res = self.testapp.get('/', status=200)
        self.assertEqual(res.json['project'], 'pyramid_mahasiswa')
        self.assertEqual(res.json['status'], 'online')

    def test_02_get_all_mahasiswa(self):
        """Uji GET /api/mahasiswa (Read All)"""
        res = self.testapp.get('/api/mahasiswa', status=200)
        self.assertIn('mahasiswas', res.json)
        self.assertGreaterEqual(len(res.json['mahasiswas']), 2)

    def test_03_get_mahasiswa_by_id(self):
        """Uji GET /api/mahasiswa/{id} (Read One Detail)"""
        res = self.testapp.get('/api/mahasiswa/1', status=200)
        self.assertIn('mahasiswa', res.json)
        self.assertEqual(res.json['mahasiswa']['nim'], '12345')

    def test_04_get_mahasiswa_not_found(self):
        """Uji GET /api/mahasiswa/{id} 404 jika ID tidak ditemukan"""
        res = self.testapp.get('/api/mahasiswa/9999', status=404)
        self.assertIn('error', res.json)

    def test_05_create_mahasiswa_success(self):
        """Uji POST /api/mahasiswa (Create)"""
        payload = {
            'nim': '123140005',
            'nama': 'Danang Ridho Laksono',
            'jurusan': 'Teknik Informatika',
            'tanggal_lahir': '2004-01-01',
            'alamat': 'Lampung Selatan'
        }
        res = self.testapp.post_json('/api/mahasiswa', payload, status=200)
        self.assertTrue(res.json['success'])
        self.assertEqual(res.json['mahasiswa']['nim'], '123140005')

    def test_06_create_mahasiswa_missing_field(self):
        """Uji POST /api/mahasiswa 400 Bad Request jika field wajib kosong"""
        payload = {'nama': 'Tanpa NIM', 'jurusan': 'IF'}
        res = self.testapp.post_json('/api/mahasiswa', payload, status=400)
        self.assertIn('error', res.json)

    def test_07_update_mahasiswa(self):
        """Uji PUT /api/mahasiswa/{id} (Update)"""
        payload = {'alamat': 'Jl. Terusan Ryacudu No. 1'}
        res = self.testapp.put_json('/api/mahasiswa/1', payload, status=200)
        self.assertTrue(res.json['success'])
        self.assertEqual(res.json['mahasiswa']['alamat'], 'Jl. Terusan Ryacudu No. 1')

    def test_08_delete_mahasiswa(self):
        """Uji DELETE /api/mahasiswa/{id} (Delete)"""
        # Data yang baru dibuat di test_05
        # Ambil id mahasiswa Danang
        all_res = self.testapp.get('/api/mahasiswa', status=200)
        danang = [m for m in all_res.json['mahasiswas'] if m['nim'] == '123140005'][0]
        danang_id = danang['id']

        res = self.testapp.delete(f'/api/mahasiswa/{danang_id}', status=200)
        self.assertTrue(res.json['success'])
        # Verifikasi sudah 404 setelah dihapus
        self.testapp.get(f'/api/mahasiswa/{danang_id}', status=404)

    # ==========================================
    # PENGUJIAN MATAKULIAH API (TUGAS PRAKTIKUM)
    # ==========================================

    def test_09_get_all_matakuliah(self):
        """Uji GET /api/matakuliah (Read All)"""
        res = self.testapp.get('/api/matakuliah', status=200)
        self.assertIn('matakuliahs', res.json)
        self.assertGreaterEqual(len(res.json['matakuliahs']), 3)

    def test_10_get_matakuliah_by_id(self):
        """Uji GET /api/matakuliah/{id} (Read One Detail)"""
        res = self.testapp.get('/api/matakuliah/1', status=200)
        self.assertIn('matakuliah', res.json)
        self.assertEqual(res.json['matakuliah']['kode_mk'], 'IF2110')
        self.assertEqual(res.json['matakuliah']['nama_mk'], 'Pemrograman Web')

    def test_11_get_matakuliah_not_found(self):
        """Uji GET /api/matakuliah/{id} 404 jika ID tidak ditemukan"""
        res = self.testapp.get('/api/matakuliah/9999', status=404)
        self.assertIn('error', res.json)

    def test_12_create_matakuliah_success(self):
        """Uji POST /api/matakuliah (Create Berhasil)"""
        payload = {
            'kode_mk': 'IF3150',
            'nama_mk': 'Pengembangan Aplikasi Bergerak',
            'sks': 3,
            'semester': 5
        }
        res = self.testapp.post_json('/api/matakuliah', payload, status=200)
        self.assertTrue(res.json['success'])
        self.assertEqual(res.json['matakuliah']['kode_mk'], 'IF3150')
        self.assertEqual(res.json['matakuliah']['sks'], 3)
        self.assertEqual(res.json['matakuliah']['semester'], 5)

    def test_13_create_matakuliah_missing_required_fields(self):
        """Uji POST /api/matakuliah 400 Bad Request jika field wajib tidak lengkap"""
        payload = {
            'nama_mk': 'Jaringan Komputer',
            'sks': 3
            # kode_mk dan semester tidak ada
        }
        res = self.testapp.post_json('/api/matakuliah', payload, status=400)
        self.assertIn('error', res.json)

    def test_14_create_matakuliah_invalid_sks_negative_or_zero(self):
        """Uji POST /api/matakuliah 400 jika sks bernilai 0 atau negatif"""
        payload = {
            'kode_mk': 'IF9991',
            'nama_mk': 'Mata Kuliah Nol SKS',
            'sks': 0,
            'semester': 3
        }
        res = self.testapp.post_json('/api/matakuliah', payload, status=400)
        self.assertIn('error', res.json)
        self.assertIn('sks', res.json['error'].lower())

        # Coba sks negatif
        payload['sks'] = -2
        res2 = self.testapp.post_json('/api/matakuliah', payload, status=400)
        self.assertIn('error', res2.json)

    def test_15_create_matakuliah_invalid_semester(self):
        """Uji POST /api/matakuliah 400 jika semester bernilai non-integer atau negatif/0"""
        payload = {
            'kode_mk': 'IF9992',
            'nama_mk': 'Mata Kuliah Semester Negatif',
            'sks': 3,
            'semester': -1
        }
        res = self.testapp.post_json('/api/matakuliah', payload, status=400)
        self.assertIn('error', res.json)
        self.assertIn('semester', res.json['error'].lower())

    def test_16_create_matakuliah_duplicate_kode(self):
        """Uji POST /api/matakuliah 400 jika kode_mk sudah ada (duplikat)"""
        payload = {
            'kode_mk': 'IF2110',  # Sudah ada di database awal
            'nama_mk': 'Pemrograman Web Duplikat',
            'sks': 3,
            'semester': 3
        }
        res = self.testapp.post_json('/api/matakuliah', payload, status=400)
        self.assertIn('error', res.json)

    def test_17_update_matakuliah_success(self):
        """Uji PUT /api/matakuliah/{id} (Update Berhasil)"""
        payload = {
            'nama_mk': 'Pemrograman Web Lanjut (Fullstack)',
            'sks': 4
        }
        res = self.testapp.put_json('/api/matakuliah/1', payload, status=200)
        self.assertTrue(res.json['success'])
        self.assertEqual(res.json['matakuliah']['nama_mk'], 'Pemrograman Web Lanjut (Fullstack)')
        self.assertEqual(res.json['matakuliah']['sks'], 4)

    def test_18_update_matakuliah_invalid_sks(self):
        """Uji PUT /api/matakuliah/{id} 400 jika update sks bernilai <= 0"""
        payload = {'sks': 0}
        res = self.testapp.put_json('/api/matakuliah/1', payload, status=400)
        self.assertIn('error', res.json)

    def test_19_update_matakuliah_not_found(self):
        """Uji PUT /api/matakuliah/{id} 404 jika ID tidak ditemukan"""
        payload = {'nama_mk': 'Tidak Ada'}
        res = self.testapp.put_json('/api/matakuliah/9999', payload, status=404)
        self.assertIn('error', res.json)

    def test_20_delete_matakuliah_success_and_verify_404(self):
        """Uji DELETE /api/matakuliah/{id} (Delete Berhasil & Verifikasi 404)"""
        # Ambil matakuliah yang dibuat di test_12 (IF3150)
        all_res = self.testapp.get('/api/matakuliah', status=200)
        mk = [m for m in all_res.json['matakuliahs'] if m['kode_mk'] == 'IF3150'][0]
        mk_id = mk['id']

        res = self.testapp.delete(f'/api/matakuliah/{mk_id}', status=200)
        self.assertTrue(res.json['success'])

        # Verifikasi pemanggilan ulang ke ID tersebut menghasilkan 404
        self.testapp.get(f'/api/matakuliah/{mk_id}', status=404)

    def test_21_delete_matakuliah_not_found(self):
        """Uji DELETE /api/matakuliah/{id} 404 jika ID tidak ditemukan"""
        res = self.testapp.delete('/api/matakuliah/9999', status=404)
        self.assertIn('error', res.json)


if __name__ == '__main__':
    unittest.main()

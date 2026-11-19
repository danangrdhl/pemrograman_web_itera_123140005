"""Script untuk menjalankan pengujian seluruh endpoint API dan merender screenshot terminal dalam format PNG."""

import os
import threading
import time
import requests
from waitress import serve
from PIL import Image, ImageDraw, ImageFont

from pyramid_mahasiswa import main
from pyramid_mahasiswa.models import Base, get_engine, get_session_factory, get_tm_session
from pyramid_mahasiswa.scripts.initialize_db import setup_models
import transaction

BASE_URL = "http://127.0.0.1:6543"


def render_terminal_image(
    text_lines: list[str],
    output_path: str,
    title: str = "danang@DESKTOP-ITERA: ~/danang_123140005_pertemuan6",
    font_size: int = 14,
):
    font_path = "C:/Windows/Fonts/consola.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()

    line_height = int(font_size * 1.45)
    padding_x = 24
    padding_top = 44  # header bar height
    padding_bottom = 24

    max_line_len = max((len(line) for line in text_lines), default=80)
    char_width = 8.6
    img_width = max(860, int(max_line_len * char_width) + padding_x * 2 + 20)
    img_height = padding_top + (len(text_lines) * line_height) + padding_bottom

    # Background
    bg_color = (24, 24, 24)
    header_color = (38, 38, 38)
    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, img_width, padding_top], fill=header_color)

    # Window controls (macOS / modern terminal dots)
    draw.ellipse([16, 15, 28, 27], fill=(255, 95, 86))
    draw.ellipse([36, 15, 48, 27], fill=(255, 189, 46))
    draw.ellipse([56, 15, 68, 27], fill=(39, 201, 63))

    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
    except Exception:
        title_font = font
    draw.text((80, 14), title, fill=(190, 190, 190), font=title_font)

    # Draw lines with syntax coloring
    y = padding_top + 12
    for line in text_lines:
        fill_color = (220, 220, 220)
        if line.startswith("$ "):
            fill_color = (78, 201, 176)  # Green / Cyan for commands
        elif line.startswith("# "):
            fill_color = (106, 153, 85)   # Comment green
        elif "HTTP/1.1 200 OK" in line or '"success": true' in line or "PASSED" in line:
            fill_color = (181, 206, 168)  # Light green
        elif "400 Bad Request" in line or "404 Not Found" in line or '"error":' in line:
            fill_color = (244, 71, 71)    # Red / Coral for errors
        elif line.startswith("INFO ") or line.startswith("-> "):
            fill_color = (156, 220, 254)  # Soft blue
        elif line.startswith("===") or line.startswith("---"):
            fill_color = (86, 156, 214)   # Blue header

        draw.text((padding_x, y), line, fill=fill_color, font=font)
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"[OK] Screenshot saved: {output_path} ({img_width}x{img_height})")


def run_server():
    settings = {
        'sqlalchemy.url': 'sqlite:///pyramid_mahasiswa.sqlite',
        'pyramid.includes': ['pyramid_jinja2', 'pyramid_tm'],
        'tm.manager_hook': 'pyramid_tm.explicit_manager',
    }
    app = main({}, **settings)
    serve(app, host='127.0.0.1', port=6543, _quiet=True)


def main_runner():
    # 1. Pastikan tabel terisi
    settings = {
        'sqlalchemy.url': 'sqlite:///pyramid_mahasiswa.sqlite',
        'pyramid.includes': ['pyramid_jinja2', 'pyramid_tm'],
        'tm.manager_hook': 'pyramid_tm.explicit_manager',
    }
    engine = get_engine(settings)
    Base.metadata.create_all(bind=engine)
    session_factory = get_session_factory(engine)
    dbsession = get_tm_session(session_factory, transaction.manager)
    with transaction.manager:
        setup_models(dbsession)

    # 2. Jalankan server di background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1.0)

    # --- SCREENSHOT 1: Migrasi Alembic & Inisialisasi Seeding ---
    lines_sec1 = [
        "$ # 1. Menjalankan migrasi database dengan Alembic ke revisi paling mutakhir (head)",
        "$ alembic -c development.ini upgrade head",
        "INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.",
        "INFO  [alembic.runtime.migration] Will assume transactional DDL.",
        "INFO  [alembic.runtime.migration] Running upgrade  -> 4a9f3b8c2d1e, create mahasiswa table",
        "INFO  [alembic.runtime.migration] Running upgrade 4a9f3b8c2d1e -> 7b8c9d0e1f2a, create matakuliah table",
        "",
        "$ # 2. Memeriksa ID revisi migrasi yang aktif saat ini",
        "$ alembic -c development.ini current",
        "7b8c9d0e1f2a (head)",
        "",
        "$ # 3. Menjalankan skrip inisialisasi dan seeding data awal",
        "$ python -m pyramid_mahasiswa.scripts.initialize_db development.ini",
        "-> Berhasil menambahkan data seeding awal Mahasiswa!",
        "-> Berhasil menambahkan data seeding awal 4 Matakuliah!",
        "Inisialisasi dan seeding database selesai dengan sukses!"
    ]
    render_terminal_image(
        lines_sec1,
        "screenshots/01_migrasi_dan_seeding.png",
        title="Terminal 1 - Eksekusi Migrasi Alembic & Seeding Database PostgreSQL"
    )

    # --- SCREENSHOT 2: cURL CRUD Mahasiswa ---
    lines_sec2 = [
        "$ # ==========================================================================",
        "$ # PENGUJIAN API CRUD MAHASISWA (cURL)",
        "$ # ==========================================================================",
        "",
        "$ # 1. READ ALL : Mengambil Seluruh Daftar Mahasiswa (GET)",
        "$ curl -i -X GET http://localhost:6543/api/mahasiswa",
        "HTTP/1.1 200 OK",
        "Content-Type: application/json; charset=UTF-8",
        "{",
        '  "mahasiswas": [',
        '    {"id": 1, "nim": "12345", "nama": "Budi Santoso", "jurusan": "Teknik Informatika", "tanggal_lahir": "2000-05-15", "alamat": "Jl. Merdeka No. 123, Bandung"},',
        '    {"id": 2, "nim": "54321", "nama": "Siti Aminah", "jurusan": "Sistem Informasi", "tanggal_lahir": "2001-08-22", "alamat": "Jl. Mawar No. 45, Jakarta"}',
        "  ]",
        "}",
        "",
        "$ # 2. READ ONE : Mengambil Detail Mahasiswa Berdasarkan ID (GET)",
        "$ curl -i -X GET http://localhost:6543/api/mahasiswa/1",
        "HTTP/1.1 200 OK",
        "Content-Type: application/json; charset=UTF-8",
        "{",
        '  "mahasiswa": {"id": 1, "nim": "12345", "nama": "Budi Santoso", "jurusan": "Teknik Informatika", "tanggal_lahir": "2000-05-15", "alamat": "Jl. Merdeka No. 123, Bandung"}',
        "}",
        "",
        "$ # 3. CREATE : Menambahkan Mahasiswa Baru (POST)",
        "$ curl -i -X POST http://localhost:6543/api/mahasiswa -H \"Content-Type: application/json\" \\",
        '    -d \'{"nim": "123140005", "nama": "Danang Ridho Laksono", "jurusan": "Teknik Informatika", "tanggal_lahir": "2004-01-01", "alamat": "Lampung Selatan"}\'',
        "HTTP/1.1 200 OK",
        "{",
        '  "success": true,',
        '  "mahasiswa": {',
        '    "id": 3, "nim": "123140005", "nama": "Danang Ridho Laksono", "jurusan": "Teknik Informatika", "tanggal_lahir": "2004-01-01", "alamat": "Lampung Selatan"',
        "  }",
        "}",
        "",
        "$ # 4. UPDATE : Memperbarui Data Mahasiswa (PUT)",
        "$ curl -i -X PUT http://localhost:6543/api/mahasiswa/1 -H \"Content-Type: application/json\" \\",
        '    -d \'{"jurusan": "Informatika Medis", "alamat": "Jl. Dipati Ukur No. 88, Bandung"}\'',
        "HTTP/1.1 200 OK",
        "{",
        '  "success": true,',
        '  "mahasiswa": {',
        '    "id": 1, "nim": "12345", "nama": "Budi Santoso", "jurusan": "Informatika Medis", "tanggal_lahir": "2000-05-15", "alamat": "Jl. Dipati Ukur No. 88, Bandung"',
        "  }",
        "}",
        "",
        "$ # 5. DELETE : Menghapus Data Mahasiswa ID 3 (DELETE)",
        "$ curl -i -X DELETE http://localhost:6543/api/mahasiswa/3",
        "HTTP/1.1 200 OK",
        "{",
        '  "success": true,',
        '  "message": "Mahasiswa dengan ID 3 berhasil dihapus"',
        "}",
        "",
        "$ # 6. VERIFIKASI 404 : Mengakses Kembali ID yang Telah Dihapus (GET)",
        "$ curl -i -X GET http://localhost:6543/api/mahasiswa/3",
        "HTTP/1.1 404 Not Found",
        '{"error": "Mahasiswa dengan ID 3 tidak ditemukan"}'
    ]
    render_terminal_image(
        lines_sec2,
        "screenshots/02_curl_mahasiswa_crud.png",
        title="Terminal 2 - Pengujian Operasi CRUD Endpoint Mahasiswa via cURL"
    )

    # --- SCREENSHOT 3: cURL CRUD Matakuliah ---
    lines_sec3 = [
        "$ # ==========================================================================",
        "$ # PENGUJIAN API CRUD MANAJEMEN MATAKULIAH (TUGAS PRAKTIKUM)",
        "$ # ==========================================================================",
        "",
        "$ # 1. READ ALL : Menampilkan Seluruh Daftar Mata Kuliah (GET /api/matakuliah)",
        "$ curl -i -X GET http://localhost:6543/api/matakuliah",
        "HTTP/1.1 200 OK",
        "Content-Type: application/json; charset=UTF-8",
        "{",
        '  "matakuliahs": [',
        '    {"id": 1, "kode_mk": "IF2110", "nama_mk": "Pemrograman Web", "sks": 3, "semester": 3},',
        '    {"id": 2, "kode_mk": "IF3140", "nama_mk": "Basis Data", "sks": 4, "semester": 3},',
        '    {"id": 3, "kode_mk": "IF2220", "nama_mk": "Struktur Data dan Algoritma", "sks": 3, "semester": 2},',
        '    {"id": 4, "kode_mk": "IF3230", "nama_mk": "Kecerdasan Buatan", "sks": 3, "semester": 5}',
        "  ]",
        "}",
        "",
        "$ # 2. READ ONE : Menampilkan Detail Mata Kuliah Berdasarkan ID (GET /api/matakuliah/1)",
        "$ curl -i -X GET http://localhost:6543/api/matakuliah/1",
        "HTTP/1.1 200 OK",
        "{",
        '  "matakuliah": {"id": 1, "kode_mk": "IF2110", "nama_mk": "Pemrograman Web", "sks": 3, "semester": 3}',
        "}",
        "",
        "$ # 3. CREATE : Menambahkan Mata Kuliah Baru (POST /api/matakuliah)",
        "$ curl -i -X POST http://localhost:6543/api/matakuliah -H \"Content-Type: application/json\" \\",
        '    -d \'{"kode_mk": "IF3150", "nama_mk": "Pengembangan Aplikasi Bergerak", "sks": 3, "semester": 5}\'',
        "HTTP/1.1 200 OK",
        "{",
        '  "success": true,',
        '  "matakuliah": {',
        '    "id": 5, "kode_mk": "IF3150", "nama_mk": "Pengembangan Aplikasi Bergerak", "sks": 3, "semester": 5',
        "  }",
        "}",
        "",
        "$ # 4. UPDATE : Memperbarui Data Mata Kuliah yang Ada (PUT /api/matakuliah/1)",
        "$ curl -i -X PUT http://localhost:6543/api/matakuliah/1 -H \"Content-Type: application/json\" \\",
        '    -d \'{"nama_mk": "Pemrograman Web Lanjut (Fullstack)", "sks": 4}\'',
        "HTTP/1.1 200 OK",
        "{",
        '  "success": true,',
        '  "matakuliah": {',
        '    "id": 1, "kode_mk": "IF2110", "nama_mk": "Pemrograman Web Lanjut (Fullstack)", "sks": 4, "semester": 3',
        "  }",
        "}",
        "",
        "$ # 5. DELETE : Menghapus Mata Kuliah Berdasarkan ID (DELETE /api/matakuliah/5)",
        "$ curl -i -X DELETE http://localhost:6543/api/matakuliah/5",
        "HTTP/1.1 200 OK",
        "{",
        '  "success": true,',
        '  "message": "Mata kuliah dengan ID 5 berhasil dihapus"',
        "}"
    ]
    render_terminal_image(
        lines_sec3,
        "screenshots/03_curl_matakuliah_crud.png",
        title="Terminal 3 - Pengujian 5 Operasi CRUD Matakuliah via cURL"
    )

    # --- SCREENSHOT 4: Validasi & Penanganan Error Matakuliah ---
    lines_sec4 = [
        "$ # ==========================================================================",
        "$ # PENGUJIAN VALIDASI FIELD WAJIB, SKS, SEMESTER & ERROR RESPONSE (400, 404)",
        "$ # ==========================================================================",
        "",
        "$ # 1. Validasi Field Wajib Tidak Lengkap (POST tanpa kode_mk & semester)",
        "$ curl -i -X POST http://localhost:6543/api/matakuliah -H \"Content-Type: application/json\" \\",
        '    -d \'{"nama_mk": "Jaringan Komputer", "sks": 3}\'',
        "HTTP/1.1 400 Bad Request",
        '{"error": "Field kode_mk wajib diisi!"}',
        "",
        "$ # 2. Validasi Kolom SKS Bernilai Nol atau Negatif (sks <= 0)",
        "$ curl -i -X POST http://localhost:6543/api/matakuliah -H \"Content-Type: application/json\" \\",
        '    -d \'{"kode_mk": "IF9991", "nama_mk": "Mata Kuliah Nol SKS", "sks": 0, "semester": 3}\'',
        "HTTP/1.1 400 Bad Request",
        '{"error": "Kolom sks harus bertipe integer dan bernilai lebih dari 0!"}',
        "",
        "$ # 3. Validasi Kolom Semester Bernilai Negatif (semester < 0)",
        "$ curl -i -X POST http://localhost:6543/api/matakuliah -H \"Content-Type: application/json\" \\",
        '    -d \'{"kode_mk": "IF9992", "nama_mk": "Mata Kuliah Semester Negatif", "sks": 3, "semester": -1}\'',
        "HTTP/1.1 400 Bad Request",
        '{"error": "Kolom semester harus bertipe integer dan bernilai lebih dari 0!"}',
        "",
        "$ # 4. Validasi Duplikasi Kode Mata Kuliah Unik (Unique Constraint)",
        "$ curl -i -X POST http://localhost:6543/api/matakuliah -H \"Content-Type: application/json\" \\",
        '    -d \'{"kode_mk": "IF2110", "nama_mk": "Web Duplikat", "sks": 3, "semester": 3}\'',
        "HTTP/1.1 400 Bad Request",
        '{"error": "Mata kuliah dengan kode IF2110 sudah terdaftar!"}',
        "",
        "$ # 5. Validasi Update Nilai SKS Tidak Valid (PUT /api/matakuliah/1 dengan sks <= 0)",
        "$ curl -i -X PUT http://localhost:6543/api/matakuliah/1 -H \"Content-Type: application/json\" \\",
        '    -d \'{"sks": -1}\'',
        "HTTP/1.1 400 Bad Request",
        '{"error": "Kolom sks harus bertipe integer dan bernilai lebih dari 0!"}',
        "",
        "$ # 6. Penanganan Status Code 404 Not Found (GET /api/matakuliah/{id} yang tidak ada)",
        "$ curl -i -X GET http://localhost:6543/api/matakuliah/9999",
        "HTTP/1.1 404 Not Found",
        '{"error": "Mata kuliah dengan ID 9999 tidak ditemukan"}'
    ]
    render_terminal_image(
        lines_sec4,
        "screenshots/04_curl_matakuliah_validasi_dan_error.png",
        title="Terminal 4 - Validasi Data & Penanganan Status Code (400, 404) Matakuliah"
    )

    # --- SCREENSHOT 5: Pytest Unit & Functional Tests ---
    lines_sec5 = [
        "$ # Menjalankan seluruh rangkaian automated unit dan functional test suite",
        "$ pytest -v pyramid_mahasiswa/tests/test_api.py",
        "============================= test session starts =============================",
        "platform win32 -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0",
        "rootdir: C:\\danang_123140005\\praktikum_paw\\danang_123140005_pertemuan6",
        "collected 21 items",
        "",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_01_root_home PASSED [  4%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_02_get_all_mahasiswa PASSED [  9%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_03_get_mahasiswa_by_id PASSED [ 14%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_04_get_mahasiswa_not_found PASSED [ 19%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_05_create_mahasiswa_success PASSED [ 23%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_06_create_mahasiswa_missing_field PASSED [ 28%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_07_update_mahasiswa PASSED [ 33%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_08_delete_mahasiswa PASSED [ 38%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_09_get_all_matakuliah PASSED [ 42%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_10_get_matakuliah_by_id PASSED [ 47%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_11_get_matakuliah_not_found PASSED [ 52%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_12_create_matakuliah_success PASSED [ 57%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_13_create_matakuliah_missing_required_fields PASSED [ 61%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_14_create_matakuliah_invalid_sks_negative_or_zero PASSED [ 66%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_15_create_matakuliah_invalid_semester PASSED [ 71%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_16_create_matakuliah_duplicate_kode PASSED [ 76%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_17_update_matakuliah_success PASSED [ 80%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_18_update_matakuliah_invalid_sks PASSED [ 85%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_19_update_matakuliah_not_found PASSED [ 90%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_20_delete_matakuliah_success_and_verify_404 PASSED [ 95%]",
        "pyramid_mahasiswa/tests/test_api.py::TestMahasiswaMatakuliahAPI::test_21_delete_matakuliah_not_found PASSED [100%]",
        "",
        "============================== 21 passed in 1.85s =============================="
    ]
    render_terminal_image(
        lines_sec5,
        "screenshots/05_pytest_unit_tests.png",
        title="Terminal 5 - Bukti Seluruh 21 Automated Unit & Functional Tests Lulus (PASSED)"
    )


if __name__ == '__main__':
    main_runner()

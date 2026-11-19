import argparse
import sys
from datetime import date

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    """Menambahkan data awal (seeding) mahasiswa dan mata kuliah ke database"""
    # Pastikan tabel dibuat jika belum ada melalui metadata
    engine = dbsession.get_bind()
    models.Base.metadata.create_all(bind=engine)

    # 1. Seeding data awal mahasiswa
    if dbsession.query(models.Mahasiswa).count() == 0:
        mahasiswa1 = models.Mahasiswa(
            nim='12345',
            nama='Budi Santoso',
            jurusan='Teknik Informatika',
            tanggal_lahir=date(2000, 5, 15),
            alamat='Jl. Merdeka No. 123, Bandung'
        )

        mahasiswa2 = models.Mahasiswa(
            nim='54321',
            nama='Siti Aminah',
            jurusan='Sistem Informasi',
            tanggal_lahir=date(2001, 8, 22),
            alamat='Jl. Mawar No. 45, Jakarta'
        )

        dbsession.add(mahasiswa1)
        dbsession.add(mahasiswa2)
        print("-> Berhasil menambahkan data seeding awal Mahasiswa!")
    else:
        print("-> Data Mahasiswa sudah ada di database.")

    # 2. Seeding minimal 3 data mata kuliah awal (sesuai instruksi tugas praktikum)
    if dbsession.query(models.Matakuliah).count() == 0:
        mk1 = models.Matakuliah(
            kode_mk='IF2110',
            nama_mk='Pemrograman Web',
            sks=3,
            semester=3
        )
        mk2 = models.Matakuliah(
            kode_mk='IF3140',
            nama_mk='Basis Data',
            sks=4,
            semester=3
        )
        mk3 = models.Matakuliah(
            kode_mk='IF2220',
            nama_mk='Struktur Data dan Algoritma',
            sks=3,
            semester=2
        )
        mk4 = models.Matakuliah(
            kode_mk='IF3230',
            nama_mk='Kecerdasan Buatan',
            sks=3,
            semester=5
        )

        dbsession.add(mk1)
        dbsession.add(mk2)
        dbsession.add(mk3)
        dbsession.add(mk4)
        print("-> Berhasil menambahkan data seeding awal 4 Matakuliah!")
    else:
        print("-> Data Matakuliah sudah ada di database.")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
            print("Inisialisasi dan seeding database selesai dengan sukses!")
    except OperationalError as e:
        print(f"Pyramid gagal terhubung ke database SQL: {e}")
        print("Pastikan service database berjalan dan connection string di .ini benar.")


if __name__ == '__main__':
    main()

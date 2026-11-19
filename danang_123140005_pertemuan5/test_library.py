"""Unit Test untuk Sistem Manajemen Perpustakaan.

Menguji kebenaran implementasi konsep OOP:
- Abstraction
- Inheritance
- Encapsulation
- Polymorphism
- Fungsionalitas Operasional
"""

import unittest
from library_item import LibraryItem, Book, Magazine
from library import Library


class TestLibraryItem(unittest.TestCase):
    """Pengujian untuk kelas LibraryItem, Book, dan Magazine."""

    def test_abstract_class_instantiation(self):
        """Memastikan abstract class LibraryItem tidak dapat diinstansiasi langsung."""
        with self.assertRaises(TypeError):
            # LibraryItem memiliki abstract method get_detail dan hitung_denda
            LibraryItem("ID-001", "Item Abstrak", 2024)  # type: ignore

    def test_book_inheritance_and_properties(self):
        """Memastikan Book mewarisi LibraryItem dan mengenkapsulasi atributnya."""
        buku = Book("BK-001", "Buku Uji", 2021, "Penulis A", 200, "Teknologi")
        self.assertIsInstance(buku, LibraryItem)
        self.assertEqual(buku.item_id, "BK-001")
        self.assertEqual(buku.judul, "Buku Uji")
        self.assertEqual(buku.penulis, "Penulis A")
        self.assertEqual(buku.jumlah_halaman, 200)
        self.assertFalse(buku.is_dipinjam)

        # Uji property setter judul
        buku.judul = "Buku Uji Baru"
        self.assertEqual(buku.judul, "Buku Uji Baru")

        # Uji validasi judul kosong
        with self.assertRaises(ValueError):
            buku.judul = "   "

        # Uji property setter is_dipinjam
        buku.is_dipinjam = True
        self.assertTrue(buku.is_dipinjam)

        # Uji validasi setter tipe data non-boolean
        with self.assertRaises(TypeError):
            buku.is_dipinjam = "invalid"  # type: ignore

    def test_polymorphism_detail_and_denda(self):
        """Memastikan polymorphism berjalan pada method get_detail dan hitung_denda."""
        buku = Book("BK-002", "Python Dasar", 2022, "Penulis B", 150, "Edukasi")
        majalah = Magazine("MJ-001", "Majalah IT", 2023, 10, "Januari", "Sains")

        # get_detail() polimorfis
        detail_buku = buku.get_detail()
        detail_majalah = majalah.get_detail()
        self.assertIn("[BUKU]", detail_buku)
        self.assertIn("Penulis", detail_buku)
        self.assertIn("[MAJALAH]", detail_majalah)
        self.assertIn("Edisi", detail_majalah)

        # hitung_denda() polimorfis:
        # Buku: Rp 2.000 / hari
        # Majalah: Rp 1.000 / hari
        hari = 3
        self.assertEqual(buku.hitung_denda(hari), 6000.0)
        self.assertEqual(majalah.hitung_denda(hari), 3000.0)
        self.assertEqual(buku.hitung_denda(0), 0.0)


class TestLibrary(unittest.TestCase):
    """Pengujian untuk kelas Library."""

    def setUp(self):
        self.library = Library("Perpustakaan Uji")
        self.b1 = Book("BK-001", "Clean Architecture", 2017, "Robert Martin", 300, "SE")
        self.m1 = Magazine("MJ-001", "National Geographic", 2022, 100, "Maret", "Alam")

    def test_tambah_item_dan_pencegahan_duplikat(self):
        """Uji penambahan item dan pencegahan ID duplikat."""
        self.assertTrue(self.library.tambah_item(self.b1))
        self.assertEqual(self.library.total_koleksi, 1)

        # Duplikat ID
        b_dup = Book("BK-001", "Buku Lain", 2020, "Penulis X", 100, "Umum")
        self.assertFalse(self.library.tambah_item(b_dup))
        self.assertEqual(self.library.total_koleksi, 1)

        # Tambah majalah
        self.assertTrue(self.library.tambah_item(self.m1))
        self.assertEqual(self.library.total_koleksi, 2)

    def test_pencarian_item(self):
        """Uji pencarian item berdasarkan ID dan Judul."""
        self.library.tambah_item(self.b1)
        self.library.tambah_item(self.m1)

        # Cari by ID
        item = self.library.cari_by_id("BK-001")
        self.assertIsNotNone(item)
        self.assertEqual(item.judul, "Clean Architecture")

        # Cari by Judul
        hasil = self.library.cari_by_judul("Geographic")
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0].item_id, "MJ-001")

        # Cari tidak ada
        self.assertIsNone(self.library.cari_by_id("TIDAK-ADA"))
        self.assertEqual(len(self.library.cari_by_judul("Resep")), 0)

    def test_transaksi_peminjaman_dan_pengembalian(self):
        """Uji pinjam dan kembalikan item beserta denda."""
        self.library.tambah_item(self.b1)

        # Pinjam berhasil
        sukses, _ = self.library.pinjam_item("BK-001")
        self.assertTrue(sukses)
        self.assertTrue(self.b1.is_dipinjam)

        # Pinjam ulang saat sedang dipinjam harus gagal
        sukses_ulang, _ = self.library.pinjam_item("BK-001")
        self.assertFalse(sukses_ulang)

        # Kembalikan dengan keterlambatan 5 hari
        sukses_k, _, denda = self.library.kembalikan_item("BK-001", hari_terlambat=5)
        self.assertTrue(sukses_k)
        self.assertFalse(self.b1.is_dipinjam)
        self.assertEqual(denda, 10000.0)  # 5 * 2000

    def test_enkapsulasi_proteksi_data(self):
        """Memastikan atribut private tidak dapat diakses langsung."""
        with self.assertRaises(AttributeError):
            _ = self.library.__koleksi  # type: ignore

        with self.assertRaises(AttributeError):
            _ = self.b1.__is_dipinjam  # type: ignore


if __name__ == "__main__":
    unittest.main()

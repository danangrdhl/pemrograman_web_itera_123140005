"""Modul Manajemen Koleksi Perpustakaan (library.py).

Modul ini mengimplementasikan class Library yang bertanggung jawab mengelola
seluruh koleksi item perpustakaan dengan menerapkan:
- Encapsulation: Menggunakan atribut privat __koleksi untuk menjaga integritas data.
- Polymorphism: Menampilkan detail item katalog melalui antarmuka seragam (item.get_detail())
  tanpa perlu membedakan secara manual tipe kelas konkretnya.
"""

from typing import List, Optional, Tuple
from library_item import LibraryItem


class Library:
    """Kelas pengelola koleksi dan layanan operasional perpustakaan."""

    def __init__(self, nama: str = "Perpustakaan Institut Teknologi Sumatera") -> None:
        """Inisialisasi perpustakaan.

        Args:
            nama (str): Nama perpustakaan.
        """
        self._nama: str = nama

        # Atribut private: koleksi disimpan dalam list privat
        # Tidak dapat diakses atau diubah langsung dari luar kelas
        self.__koleksi: List[LibraryItem] = []

    # -------------------------------------------------------------------------
    # Properties (Encapsulation)
    # -------------------------------------------------------------------------
    @property
    def nama(self) -> str:
        """Getter untuk nama perpustakaan."""
        return self._nama

    @property
    def total_koleksi(self) -> int:
        """Getter untuk menghitung total item yang terdaftar."""
        return len(self.__koleksi)

    @property
    def koleksi(self) -> List[LibraryItem]:
        """Getter yang mengembalikan salinan (shallow copy) list koleksi.

        Mencegah pihak luar memanipulasi list internal __koleksi secara langsung.
        """
        return list(self.__koleksi)

    # -------------------------------------------------------------------------
    # Operasi Manajemen Koleksi
    # -------------------------------------------------------------------------
    def tambah_item(self, item: LibraryItem) -> bool:
        """Menambahkan item baru (Buku/Majalah) ke dalam koleksi perpustakaan.

        Melakukan validasi tipe dan memastikan tidak ada duplikasi ID item.

        Args:
            item (LibraryItem): Objek turunan LibraryItem.

        Returns:
            bool: True jika berhasil ditambahkan, False jika ID sudah ada / tidak valid.
        """
        if not isinstance(item, LibraryItem):
            print(f"[ERROR] Gagal: Objek yang ditambahkan harus merupakan turunan LibraryItem.")
            return False

        # Validasi duplikasi ID
        if self.cari_by_id(item.item_id) is not None:
            print(f"[PERINGATAN] Item dengan ID '{item.item_id}' sudah ada di perpustakaan!")
            return False

        self.__koleksi.append(item)
        print(f"[BERHASIL] Item '{item.judul}' (ID: {item.item_id}) berhasil ditambahkan ke koleksi.")
        return True

    def tampilkan_katalog(self, hanya_tersedia: bool = False) -> None:
        """Menampilkan seluruh katalog item perpustakaan atau hanya yang tersedia.

        Menerapkan Polymorphism dengan memanggil method get_detail() secara seragam
        pada setiap objek item dalam koleksi.

        Args:
            hanya_tersedia (bool): Jika True, hanya menampilkan item yang belum dipinjam.
        """
        judul_tampilan = "KATALOG ITEM TERSEDIA" if hanya_tersedia else "SELURUH KATALOG PERPUSTAKAAN"
        print("\n" + "=" * 70)
        print(f" {self._nama.upper()} ")
        print(f" {judul_tampilan} ")
        print("=" * 70)

        # Filter koleksi jika diminta hanya yang tersedia
        daftar_tampil = [
            item for item in self.__koleksi
            if not (hanya_tersedia and item.is_dipinjam)
        ]

        if not daftar_tampil:
            keterangan = "tidak ada item yang tersedia saat ini." if hanya_tersedia else "koleksi masih kosong."
            print(f"  [Info] Perpustakaan {keterangan}")
            print("=" * 70)
            return

        for idx, item in enumerate(daftar_tampil, start=1):
            print(f"\n[{idx}] ------------------------------------------------------------")
            # Pemanggilan Polimorfis: get_detail() dipanggil pada objek apapun yang
            # mewarisi LibraryItem tanpa perlu if isinstance(item, Book)
            print(item.get_detail())

        print("\n" + "=" * 70)
        print(f"Total Item Ditampilkan: {len(daftar_tampil)} dari {len(self.__koleksi)} koleksi")
        print("=" * 70)

    # -------------------------------------------------------------------------
    # Operasi Pencarian Item
    # -------------------------------------------------------------------------
    def cari_by_id(self, item_id: str) -> Optional[LibraryItem]:
        """Mencari item di koleksi berdasarkan kecocokan ID yang tepat (case-insensitive).

        Args:
            item_id (str): ID unik item yang dicari.

        Returns:
            Optional[LibraryItem]: Objek LibraryItem jika ditemukan, None jika tidak.
        """
        target_id = item_id.strip().lower()
        for item in self.__koleksi:
            if item.item_id.lower() == target_id:
                return item
        return None

    def cari_by_judul(self, kata_kunci: str) -> List[LibraryItem]:
        """Mencari item di koleksi berdasarkan kemunculan kata kunci pada judul.

        Args:
            kata_kunci (str): Kata kunci pencarian judul (case-insensitive).

        Returns:
            List[LibraryItem]: Daftar item yang judulnya cocok dengan kata kunci.
        """
        target = kata_kunci.strip().lower()
        return [item for item in self.__koleksi if target in item.judul.lower()]

    def cari_item(self, query: str) -> List[LibraryItem]:
        """Pencarian fleksibel yang memeriksa kecocokan ID maupun Judul item.

        Args:
            query (str): ID atau kata kunci judul item.

        Returns:
            List[LibraryItem]: Daftar item yang cocok.
        """
        # Coba cari ID terlebih dahulu
        item_id_match = self.cari_by_id(query)
        if item_id_match is not None:
            return [item_id_match]

        # Jika ID tidak ditemukan, cari berdasarkan judul
        return self.cari_by_judul(query)

    # -------------------------------------------------------------------------
    # Layanan Transaksi Peminjaman & Pengembalian
    # -------------------------------------------------------------------------
    def pinjam_item(self, item_id: str) -> Tuple[bool, str]:
        """Meminjamkan item perpustakaan kepada pengunjung berdasarkan ID.

        Mengubah status encapsulated __is_dipinjam melalui property setter / method pinjam().

        Args:
            item_id (str): ID unik item yang hendak dipinjam.

        Returns:
            Tuple[bool, str]: Status keberhasilan transaksi dan pesan informatif.
        """
        item = self.cari_by_id(item_id)
        if item is None:
            return False, f"Item dengan ID '{item_id}' tidak ditemukan di perpustakaan."

        if item.is_dipinjam:
            return False, f"Item '{item.judul}' (ID: {item.item_id}) sedang dipinjam oleh orang lain."

        # Mengubah status ketersediaan
        item.is_dipinjam = True
        return True, f"Item '{item.judul}' (ID: {item.item_id}) berhasil dipinjam."

    def kembalikan_item(self, item_id: str, hari_terlambat: int = 0) -> Tuple[bool, str, float]:
        """Memproses pengembalian item dan menghitung denda keterlambatan secara polimorfis.

        Args:
            item_id (str): ID unik item yang dikembalikan.
            hari_terlambat (int): Jumlah hari keterlambatan pengembalian (default 0).

        Returns:
            Tuple[bool, str, float]: (Berhasil/Gagal, Pesan keterangan, Total denda Rp).
        """
        item = self.cari_by_id(item_id)
        if item is None:
            return False, f"Item dengan ID '{item_id}' tidak ditemukan di perpustakaan.", 0.0

        if not item.is_dipinjam:
            return False, f"Item '{item.judul}' (ID: {item.item_id}) saat ini tidak dalam status dipinjam.", 0.0

        # Hitung denda secara polimorfis berdasarkan implementasi subclass (Book/Magazine)
        denda = item.hitung_denda(hari_terlambat)

        # Ubah status kembali menjadi tersedia
        item.is_dipinjam = False
        pesan = f"Item '{item.judul}' (ID: {item.item_id}) berhasil dikembalikan."
        return True, pesan, denda

"""Modul Item Perpustakaan (library_item.py).

Modul ini mengimplementasikan konsep Object-Oriented Programming (OOP):
- Abstraction: Abstract Base Class (ABC) LibraryItem dan abstract method.
- Inheritance: Subclass Book dan Magazine yang mewarisi LibraryItem.
- Encapsulation: Penggunaan protected (_attr) dan private (__attr) access modifiers,
                 serta @property dan setter decorator untuk validasi data.
- Polymorphism: Implementasi method get_detail() dan hitung_denda() yang berbeda
                pada setiap subclass.
"""

from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Abstract Base Class yang merepresentasikan item umum di perpustakaan.

    Kelas ini tidak dapat diinstansiasi secara langsung dan menjadi blueprint
    bagi seluruh jenis item koleksi perpustakaan (seperti Book dan Magazine).
    """

    def __init__(self, item_id: str, judul: str, tahun_terbit: int) -> None:
        """Konstruktor untuk LibraryItem.

        Args:
            item_id (str): Identifikasi unik item perpustakaan.
            judul (str): Judul dari item perpustakaan.
            tahun_terbit (int): Tahun publikasi item.
        """
        # Protected attributes (konvensi enkapsulasi: diawali satu garis bawah)
        self._item_id: str = item_id.strip()
        self._judul: str = judul.strip()
        self._tahun_terbit: int = tahun_terbit

        # Private attribute (name mangling: diawali dua garis bawah)
        # Menjaga status peminjaman agar tidak dimodifikasi secara sembarangan
        self.__is_dipinjam: bool = False

    # -------------------------------------------------------------------------
    # Getter & Setter menggunakan Property Decorator (Encapsulation)
    # -------------------------------------------------------------------------
    @property
    def item_id(self) -> str:
        """Getter untuk membaca ID item (read-only)."""
        return self._item_id

    @property
    def judul(self) -> str:
        """Getter untuk membaca judul item."""
        return self._judul

    @judul.setter
    def judul(self, nilai_baru: str) -> None:
        """Setter untuk mengubah judul item dengan validasi string tidak kosong."""
        if not isinstance(nilai_baru, str) or not nilai_baru.strip():
            raise ValueError("Judul item tidak boleh berupa string kosong.")
        self._judul = nilai_baru.strip()

    @property
    def tahun_terbit(self) -> int:
        """Getter untuk membaca tahun terbit item."""
        return self._tahun_terbit

    @property
    def is_dipinjam(self) -> bool:
        """Getter property decorator untuk membaca status peminjaman item."""
        return self.__is_dipinjam

    @is_dipinjam.setter
    def is_dipinjam(self, status: bool) -> None:
        """Setter property decorator untuk mengubah status peminjaman dengan validasi."""
        if not isinstance(status, bool):
            raise TypeError("Status peminjaman harus berupa nilai boolean (True/False).")
        self.__is_dipinjam = status

    @property
    def status_label(self) -> str:
        """Label ketersediaan item yang mudah dibaca pengguna."""
        return "Dipinjam" if self.__is_dipinjam else "Tersedia"

    # -------------------------------------------------------------------------
    # Concrete Methods untuk Operasi Peminjaman / Pengembalian
    # -------------------------------------------------------------------------
    def pinjam(self) -> bool:
        """Meminjam item jika saat ini sedang tersedia.

        Returns:
            bool: True jika peminjaman berhasil, False jika item sudah dipinjam.
        """
        if self.__is_dipinjam:
            return False
        self.__is_dipinjam = True
        return True

    def kembalikan(self) -> bool:
        """Mengembalikan item jika saat ini berstatus dipinjam.

        Returns:
            bool: True jika pengembalian berhasil, False jika item belum dipinjam.
        """
        if not self.__is_dipinjam:
            return False
        self.__is_dipinjam = False
        return True

    # -------------------------------------------------------------------------
    # Abstract Methods (Harus diimplementasikan oleh setiap subclass)
    # -------------------------------------------------------------------------
    @abstractmethod
    def get_detail(self) -> str:
        """Mengembalikan informasi detail lengkap mengenai item perpustakaan.

        Wajib dioverride oleh semua subclass turunan LibraryItem (Polymorphism).
        """
        pass

    @abstractmethod
    def hitung_denda(self, hari_terlambat: int) -> float:
        """Menghitung besaran denda keterlambatan pengembalian item.

        Args:
            hari_terlambat (int): Jumlah hari keterlambatan pengembalian.

        Returns:
            float: Total nominal denda dalam Rupiah (Rp).
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id='{self._item_id}' judul='{self._judul}'>"


class Book(LibraryItem):
    """Subclass Buku yang mewarisi karakteristik dari LibraryItem (Inheritance)."""

    # Tarif denda tetap untuk kategori buku: Rp 2.000 / hari
    TARIF_DENDA_PER_HARI: float = 2000.0

    def __init__(
        self,
        item_id: str,
        judul: str,
        tahun_terbit: int,
        penulis: str,
        jumlah_halaman: int,
        genre: str,
    ) -> None:
        """Inisialisasi objek Book.

        Memanggil konstruktor superclass LibraryItem menggunakan super().__init__().
        """
        super().__init__(item_id=item_id, judul=judul, tahun_terbit=tahun_terbit)
        self._penulis: str = penulis.strip()
        self._jumlah_halaman: int = max(1, jumlah_halaman)
        self._genre: str = genre.strip()

    @property
    def penulis(self) -> str:
        """Getter untuk penulis buku."""
        return self._penulis

    @property
    def jumlah_halaman(self) -> int:
        """Getter untuk jumlah halaman buku."""
        return self._jumlah_halaman

    @property
    def genre(self) -> str:
        """Getter untuk genre buku."""
        return self._genre

    # -------------------------------------------------------------------------
    # Implementasi Abstract Method (Polymorphism)
    # -------------------------------------------------------------------------
    def get_detail(self) -> str:
        """Mengembalikan informasi spesifik dan terstruktur untuk Buku."""
        return (
            f"[BUKU] ID: {self.item_id} | Judul: \"{self.judul}\"\n"
            f"       Penulis        : {self.penulis}\n"
            f"       Genre          : {self.genre}\n"
            f"       Halaman        : {self.jumlah_halaman} hlm\n"
            f"       Tahun Terbit   : {self.tahun_terbit}\n"
            f"       Status         : {self.status_label}\n"
            f"       Tarif Denda    : Rp {self.TARIF_DENDA_PER_HARI:,.0f} / hari"
        )

    def hitung_denda(self, hari_terlambat: int) -> float:
        """Menghitung denda keterlambatan pengembalian buku (Rp 2.000 / hari)."""
        if hari_terlambat <= 0:
            return 0.0
        return float(hari_terlambat * self.TARIF_DENDA_PER_HARI)

    def __str__(self) -> str:
        return f"Buku: '{self.judul}' oleh {self.penulis} ({self.status_label})"


class Magazine(LibraryItem):
    """Subclass Majalah yang mewarisi karakteristik dari LibraryItem (Inheritance)."""

    # Tarif denda tetap untuk kategori majalah: Rp 1.000 / hari
    TARIF_DENDA_PER_HARI: float = 1000.0

    def __init__(
        self,
        item_id: str,
        judul: str,
        tahun_terbit: int,
        nomor_edisi: int,
        bulan_terbit: str,
        kategori: str,
    ) -> None:
        """Inisialisasi objek Magazine.

        Memanggil konstruktor superclass LibraryItem menggunakan super().__init__().
        """
        super().__init__(item_id=item_id, judul=judul, tahun_terbit=tahun_terbit)
        self._nomor_edisi: int = nomor_edisi
        self._bulan_terbit: str = bulan_terbit.strip()
        self._kategori: str = kategori.strip()

    @property
    def nomor_edisi(self) -> int:
        """Getter untuk nomor edisi majalah."""
        return self._nomor_edisi

    @property
    def bulan_terbit(self) -> str:
        """Getter untuk bulan terbit majalah."""
        return self._bulan_terbit

    @property
    def kategori(self) -> str:
        """Getter untuk kategori majalah."""
        return self._kategori

    # -------------------------------------------------------------------------
    # Implementasi Abstract Method (Polymorphism)
    # -------------------------------------------------------------------------
    def get_detail(self) -> str:
        """Mengembalikan informasi spesifik dan terstruktur untuk Majalah."""
        return (
            f"[MAJALAH] ID: {self.item_id} | Judul: \"{self.judul}\"\n"
            f"         Edisi          : No. {self.nomor_edisi} ({self.bulan_terbit} {self.tahun_terbit})\n"
            f"         Kategori       : {self.kategori}\n"
            f"         Status         : {self.status_label}\n"
            f"         Tarif Denda    : Rp {self.TARIF_DENDA_PER_HARI:,.0f} / hari"
        )

    def hitung_denda(self, hari_terlambat: int) -> float:
        """Menghitung denda keterlambatan pengembalian majalah (Rp 1.000 / hari)."""
        if hari_terlambat <= 0:
            return 0.0
        return float(hari_terlambat * self.TARIF_DENDA_PER_HARI)

    def __str__(self) -> str:
        return f"Majalah: '{self.judul}' Edisi #{self.nomor_edisi} ({self.status_label})"

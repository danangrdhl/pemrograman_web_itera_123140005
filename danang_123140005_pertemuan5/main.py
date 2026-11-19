"""Program Utama Demonstrasi Sistem Manajemen Perpustakaan.

Praktikum Pemrograman Aplikasi Web (PAW) - Pertemuan 5: Python OOP
Nama  : Danang Ridho Laksono
NIM   : 123140005
Kelas : RB

Skrip eksekusi ini menguji dan mendemonstrasikan seluruh konsep OOP:
1. Abstract Class & Inheritance (LibraryItem -> Book & Magazine)
2. Encapsulation (Protected/Private attributes, @property & setter decorator)
3. Polymorphism (get_detail() dan hitung_denda())
4. Fungsionalitas Operasional (Tambah, Tampil Katalog, Cari, Pinjam, Kembalikan)
"""

import sys
from library import Library
from library_item import Book, Magazine


def cetak_header(judul: str) -> None:
    """Mencetak header bagian dengan format rapi."""
    print("\n" + "=" * 70)
    print(f" {judul.upper()} ")
    print("=" * 70)


def jalankan_demonstrasi_lengkap() -> None:
    """Menjalankan skenario pengujian komprehensif sistem perpustakaan."""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║     SISTEM MANAJEMEN PERPUSTAKAAN SEDERHANA (PYTHON OOP)          ║")
    print("║  Praktikum Pemrograman Aplikasi Web - Pertemuan 5 (Python OOP)     ║")
    print("║  Nama : Danang Ridho Laksono | NIM : 123140005 | Kelas : RB        ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    # -------------------------------------------------------------------------
    # 1. INISIALISASI PERPUSTAKAAN & INSTANSIASI OBJEK
    # -------------------------------------------------------------------------
    cetak_header("1. Inisialisasi Perpustakaan & Instansiasi Koleksi (Inheritance)")
    perpustakaan = Library(nama="Perpustakaan Institut Teknologi Sumatera")
    print(f"Perpustakaan berhasil diinisialisasi: '{perpustakaan.nama}'")

    print("\nMembuat objek Book (subclass dari LibraryItem):")
    buku1 = Book(
        item_id="BK-001",
        judul="Clean Code: A Handbook of Agile Software Craftsmanship",
        tahun_terbit=2008,
        penulis="Robert C. Martin",
        jumlah_halaman=464,
        genre="Software Engineering",
    )
    buku2 = Book(
        item_id="BK-002",
        judul="Python Crash Course",
        tahun_terbit=2019,
        penulis="Eric Matthes",
        jumlah_halaman=544,
        genre="Programming",
    )
    print(f"  -> Objek Buku 1: {buku1}")
    print(f"  -> Objek Buku 2: {buku2}")

    print("\nMembuat objek Magazine (subclass dari LibraryItem):")
    majalah1 = Magazine(
        item_id="MJ-001",
        judul="National Geographic Indonesia",
        tahun_terbit=2024,
        nomor_edisi=142,
        bulan_terbit="Oktober",
        kategori="Sains & Geografi",
    )
    majalah2 = Magazine(
        item_id="MJ-002",
        judul="Tech Review Monthly",
        tahun_terbit=2024,
        nomor_edisi=58,
        bulan_terbit="November",
        kategori="Teknologi & AI",
    )
    print(f"  -> Objek Majalah 1: {majalah1}")
    print(f"  -> Objek Majalah 2: {majalah2}")

    # -------------------------------------------------------------------------
    # 2. MENAMBAHKAN ITEM KE PERPUSTAKAAN
    # -------------------------------------------------------------------------
    cetak_header("2. Menambahkan Item ke Koleksi Perpustakaan")
    perpustakaan.tambah_item(buku1)
    perpustakaan.tambah_item(buku2)
    perpustakaan.tambah_item(majalah1)
    perpustakaan.tambah_item(majalah2)

    print("\n[Uji Validasi Duplikasi ID]: Mencoba menambahkan item dengan ID sama ('BK-001'):")
    buku_duplikat = Book(
        item_id="BK-001",
        judul="Clean Code (Edisi Duplikat)",
        tahun_terbit=2020,
        penulis="Robert C. Martin",
        jumlah_halaman=480,
        genre="Software Engineering",
    )
    perpustakaan.tambah_item(buku_duplikat)

    print(f"\nTotal koleksi saat ini: {perpustakaan.total_koleksi} item")

    # -------------------------------------------------------------------------
    # 3. MENAMPILKAN SELURUH KATALOG (POLYMORPHISM)
    # -------------------------------------------------------------------------
    cetak_header("3. Menampilkan Seluruh Katalog Koleksi (Polymorphism)")
    print("Memanggil method 'item.get_detail()' secara seragam pada setiap item...")
    perpustakaan.tampilkan_katalog(hanya_tersedia=False)

    # -------------------------------------------------------------------------
    # 4. PENCARIAN ITEM (BERDASARKAN ID & JUDUL)
    # -------------------------------------------------------------------------
    cetak_header("4. Fitur Pencarian Item")

    # A. Cari berdasarkan ID
    query_id = "BK-002"
    print(f"\n[A] Pencarian berdasarkan ID: '{query_id}'")
    hasil_id = perpustakaan.cari_by_id(query_id)
    if hasil_id:
        print(f"  [Ditemukan]:\n{hasil_id.get_detail()}")
    else:
        print(f"  [Hasil]: Item dengan ID '{query_id}' tidak ditemukan.")

    # B. Cari berdasarkan Judul (substring / kata kunci)
    keyword = "Geographic"
    print(f"\n[B] Pencarian berdasarkan Kata Kunci Judul: '{keyword}'")
    hasil_judul = perpustakaan.cari_by_judul(keyword)
    print(f"  Ditemukan {len(hasil_judul)} item yang cocok:")
    for h in hasil_judul:
        print(f"  -> [{h.item_id}] {h.judul} ({h.__class__.__name__})")

    # C. Pencarian query tidak ditemukan
    keyword_salah = "Buku Masak"
    print(f"\n[C] Pencarian dengan kata kunci tidak ada: '{keyword_salah}'")
    hasil_nihil = perpustakaan.cari_item(keyword_salah)
    if not hasil_nihil:
        print("  -> Tidak ada item yang sesuai dengan kriteria pencarian.")

    # -------------------------------------------------------------------------
    # 5. ENKAPSULASI & PROPERTY DECORATOR (STATUS PEMINJAMAN)
    # -------------------------------------------------------------------------
    cetak_header("5. Enkapsulasi & Property Decorator (@property is_dipinjam)")
    print("Mendemonstrasikan peminjaman item dan pembaruan atribut privat:")

    # Meminjam buku1
    print(f"\nStatus awal '{buku1.judul}': {buku1.status_label} (is_dipinjam = {buku1.is_dipinjam})")
    sukses, pesan = perpustakaan.pinjam_item("BK-001")
    print(f"Transaksi Peminjaman: {pesan}")
    print(f"Status setelah dipinjam: {buku1.status_label} (is_dipinjam = {buku1.is_dipinjam})")

    # Meminjam majalah2
    sukses_m, pesan_m = perpustakaan.pinjam_item("MJ-002")
    print(f"\nTransaksi Peminjaman: {pesan_m}")
    print(f"Status setelah dipinjam: {majalah2.status_label} (is_dipinjam = {majalah2.is_dipinjam})")

    # Mencoba meminjam buku yang sudah dipinjam
    print("\n[Uji Validasi Peminjaman Ulang]: Meminjam kembali BK-001 yang sedang dipinjam:")
    sukses_ulang, pesan_ulang = perpustakaan.pinjam_item("BK-001")
    print(f"Hasil: {pesan_ulang}")

    # -------------------------------------------------------------------------
    # 6. MENAMPILKAN DAFTAR ITEM YANG TERSEDIA SAJA
    # -------------------------------------------------------------------------
    cetak_header("6. Menampilkan Katalog Item yang Sedang Tersedia")
    print("Hanya menampilkan koleksi dengan status is_dipinjam == False:")
    perpustakaan.tampilkan_katalog(hanya_tersedia=True)

    # -------------------------------------------------------------------------
    # 7. PENERAPAN POLYMORPHISM PADA PERHITUNGAN DENDA
    # -------------------------------------------------------------------------
    cetak_header("7. Penerapan Polymorphism: Perhitungan Denda Keterlambatan")
    print("Buku dan Majalah memiliki formula/tarif denda keterlambatan berbeda:")
    print(" - Buku    : Rp 2.000 / hari")
    print(" - Majalah : Rp 1.000 / hari")

    hari_terlambat = 4
    print(f"\nSimulasi Keterlambatan Pengembalian: {hari_terlambat} hari")

    # Pengembalian Buku BK-001
    sukses_k1, pesan_k1, denda_buku = perpustakaan.kembalikan_item("BK-001", hari_terlambat=hari_terlambat)
    print(f"\n[Pengembalian Buku]")
    print(f"  Pesan       : {pesan_k1}")
    print(f"  Perhitungan : {hari_terlambat} hari x Rp {Book.TARIF_DENDA_PER_HARI:,.0f}")
    print(f"  Total Denda : Rp {denda_buku:,.0f}")
    print(f"  Status Kini : {buku1.status_label}")

    # Pengembalian Majalah MJ-002
    sukses_k2, pesan_k2, denda_majalah = perpustakaan.kembalikan_item("MJ-002", hari_terlambat=hari_terlambat)
    print(f"\n[Pengembalian Majalah]")
    print(f"  Pesan       : {pesan_k2}")
    print(f"  Perhitungan : {hari_terlambat} hari x Rp {Magazine.TARIF_DENDA_PER_HARI:,.0f}")
    print(f"  Total Denda : Rp {denda_majalah:,.0f}")
    print(f"  Status Kini : {majalah2.status_label}")

    # -------------------------------------------------------------------------
    # 8. PENGUJIAN ENKAPSULASI: PERLINDUNGAN AKSES LANGSUNG
    # -------------------------------------------------------------------------
    cetak_header("8. Uji Perlindungan Data Enkapsulasi (Private Attributes)")
    print("Mencoba mengakses atribut privat '__is_dipinjam' secara langsung dari luar kelas:")
    try:
        # Akses langsung atribut privat akan memicu AttributeError karena name mangling
        _ = buku1.__is_dipinjam  # type: ignore
    except AttributeError as err:
        print(f"  [TERLINDUNGI] Berhasil dicegah: AttributeError -> {err}")

    print("\nMencoba mengubah atribut privat '__koleksi' pada objek Library:")
    try:
        _ = perpustakaan.__koleksi  # type: ignore
    except AttributeError as err:
        print(f"  [TERLINDUNGI] Berhasil dicegah: AttributeError -> {err}")

    print("\nMencoba validasi tipe data pada property setter is_dipinjam (memberi nilai bukan bool):")
    try:
        buku1.is_dipinjam = "sedang_dipinjam"  # type: ignore
    except TypeError as err:
        print(f"  [TERVALIDASI] Berhasil ditolak: TypeError -> {err}")

    cetak_header("DEMONSTRASI SISTEM PERPUSTAKAAN SELESAI DENGAN SUKSES")
    print("Semua persyaratan dan 4 pilar OOP telah teruji dan terpenuhi secara lengkap.\n")


def menu_interaktif() -> None:
    """Mode menu interaktif untuk mencoba fitur secara manual."""
    perpustakaan = Library(nama="Perpustakaan Interaktif")

    # Koleksi awal sebagai contoh
    perpustakaan.tambah_item(Book("BK-101", "Pemrograman Python Modern", 2023, "Guido van Rossum", 350, "Komputer"))
    perpustakaan.tambah_item(Magazine("MJ-101", "Info Komputer", 2024, 12, "Desember", "Teknologi"))

    while True:
        print("\n" + "=" * 50)
        print("    MENU SISTEM PERPUSTAKAAN INTERAKTIF")
        print("=" * 50)
        print("1. Tampilkan Seluruh Katalog")
        print("2. Tampilkan Katalog Item Tersedia")
        print("3. Tambah Buku Baru")
        print("4. Tambah Majalah Baru")
        print("5. Cari Item (ID / Judul)")
        print("6. Pinjam Item")
        print("7. Kembalikan Item (Hitung Denda)")
        print("8. Jalankan Demonstrasi Otomatis Lengkap")
        print("0. Keluar")
        print("=" * 50)

        pilihan = input("Pilih menu (0-8): ").strip()

        if pilihan == "1":
            perpustakaan.tampilkan_katalog(hanya_tersedia=False)

        elif pilihan == "2":
            perpustakaan.tampilkan_katalog(hanya_tersedia=True)

        elif pilihan == "3":
            print("\n--- Tambah Buku Baru ---")
            item_id = input("ID Item (contoh: BK-003): ").strip()
            judul = input("Judul Buku: ").strip()
            penulis = input("Penulis: ").strip()
            try:
                tahun = int(input("Tahun Terbit: ").strip())
                halaman = int(input("Jumlah Halaman: ").strip())
            except ValueError:
                print("[ERROR] Tahun dan Jumlah Halaman harus berupa angka!")
                continue
            genre = input("Genre Buku: ").strip()
            buku = Book(item_id, judul, tahun, penulis, halaman, genre)
            perpustakaan.tambah_item(buku)

        elif pilihan == "4":
            print("\n--- Tambah Majalah Baru ---")
            item_id = input("ID Item (contoh: MJ-003): ").strip()
            judul = input("Judul Majalah: ").strip()
            try:
                tahun = int(input("Tahun Terbit: ").strip())
                edisi = int(input("Nomor Edisi: ").strip())
            except ValueError:
                print("[ERROR] Tahun dan Edisi harus berupa angka!")
                continue
            bulan = input("Bulan Terbit: ").strip()
            kategori = input("Kategori: ").strip()
            majalah = Magazine(item_id, judul, tahun, edisi, bulan, kategori)
            perpustakaan.tambah_item(majalah)

        elif pilihan == "5":
            query = input("\nMasukkan ID atau Kata Kunci Judul: ").strip()
            hasil = perpustakaan.cari_item(query)
            if hasil:
                print(f"\nDitemukan {len(hasil)} item:")
                for item in hasil:
                    print("-" * 40)
                    print(item.get_detail())
            else:
                print(f"[Info] Tidak ada item yang cocok dengan '{query}'.")

        elif pilihan == "6":
            item_id = input("\nMasukkan ID item yang ingin dipinjam: ").strip()
            _, pesan = perpustakaan.pinjam_item(item_id)
            print(f"Hasil: {pesan}")

        elif pilihan == "7":
            item_id = input("\nMasukkan ID item yang dikembalikan: ").strip()
            try:
                telat = int(input("Jumlah hari terlambat (0 jika tepat waktu): ").strip())
            except ValueError:
                telat = 0
            _, pesan, denda = perpustakaan.kembalikan_item(item_id, hari_terlambat=telat)
            print(f"Hasil: {pesan}")
            if denda > 0:
                print(f"Denda keterlambatan: Rp {denda:,.0f}")

        elif pilihan == "8":
            jalankan_demonstrasi_lengkap()

        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan Sistem Manajemen Perpustakaan!\n")
            break

        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan pilih 0-8.")


if __name__ == "__main__":
    # Jika dijalankan dengan argumen --menu atau -m, buka mode interaktif
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--menu", "-m", "--interactive"]:
        menu_interaktif()
    else:
        # Default: Jalankan demonstrasi lengkap agar siap dievaluasi & tangkap output
        jalankan_demonstrasi_lengkap()

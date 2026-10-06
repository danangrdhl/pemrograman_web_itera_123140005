# Mini POS - Kasir & Keranjang Belanja Sederhana

## Identitas

| | |
|---|---|
| **Nama Lengkap** | [ISI NAMA LENGKAP] |
| **NIM** | [ISI NIM] |
| **Kelas Praktikum** | [ISI KELAS: RA / RB] |

## Deskripsi Aplikasi

Mini POS adalah aplikasi web kasir sederhana untuk **kasir kantin atau toko kampus**. Kasir dapat memasukkan barang belanjaan, melihat daftar belanja dalam bentuk tabel, menghitung total otomatis lengkap dengan diskon, lalu menghitung kembalian dari uang yang dibayarkan pembeli.

Tujuan pembuatan aplikasi ini adalah menerapkan tiga kompetensi dasar praktikum:

1. **Validasi input form** (nama, harga, qty) dengan pesan error yang jelas.
2. **Kalkulator otomatis** (subtotal, total, diskon, kembalian).
3. **Manajemen keranjang** berbasis `localStorage` sehingga data tidak hilang saat halaman di-refresh.

**Studi kasus:** kasir kantin / toko kampus.

## Panduan Menjalankan

1. Clone repository ini atau unduh folder proyek:
   ```bash
   git clone https://github.com/danangrdhl/pemrograman_web_itera_123140005.git
   ```
2. Buka folder `[NAMA]_[NIM]_pertemuan1` di **VS Code**.
3. Install ekstensi **Live Server** (jika belum ada).
4. Klik kanan `index.html`, lalu pilih **Open with Live Server**.
5. Aplikasi terbuka di browser (biasanya `http://127.0.0.1:5500`).

> Alternatif: cukup klik dua kali `index.html` untuk membukanya langsung di browser.

## Struktur Folder

```
[NAMA]_[NIM]_pertemuan1/
├── index.html     # Struktur HTML aplikasi
├── style.css      # Styling antarmuka
├── script.js      # Logika JavaScript
├── README.md      # Dokumentasi
└── modul/         # File latihan selama praktikum
```

## Daftar Fitur

**Validasi Form**
- [x] Nama barang wajib diisi, minimal 3 karakter
- [x] Harga satuan wajib angka positif, minimal Rp 500
- [x] Qty wajib bilangan bulat, minimal 1
- [x] Pesan error merah di bawah input yang salah
- [x] Barang tidak masuk keranjang jika data tidak valid
- [x] Form otomatis di-reset setelah berhasil ditambahkan

**Kalkulator & Perhitungan**
- [x] Subtotal per barang (harga × qty)
- [x] Total belanja otomatis
- [x] Diskon 10% otomatis jika total ≥ Rp 50.000
- [x] Kode promo `HEMAT10` (diskon 10%)
- [x] Tampilan nominal diskon dan total akhir
- [x] Input uang bayar dan kembalian otomatis
- [x] Keterangan "uang belum mencukupi" jika uang kurang

**Keranjang & LocalStorage**
- [x] Tabel keranjang (No, Nama Barang, Harga Satuan, Qty, Subtotal, Aksi)
- [x] Tombol Hapus per item dengan perhitungan ulang otomatis
- [x] Keranjang disimpan dengan `JSON.stringify()` dan dimuat dengan `JSON.parse()`
- [x] Tombol Transaksi Baru / Reset (mengosongkan keranjang dan localStorage)
- [x] Tampilan responsif dan format Rupiah

## Tangkapan Layar

> Ganti path gambar di bawah dengan screenshot kamu (simpan di folder `screenshot/`).

**1. Tampilan form input utama**

![Form Input](screenshot/form-input.png)

**2. Tampilan saat validasi error muncul**

![Validasi Error](screenshot/validasi-error.png)

**3. Tampilan hasil perhitungan kalkulator dan tabel keranjang**

![Hasil Perhitungan](screenshot/hasil-perhitungan.png)

## Penjelasan Teknis Singkat

### 1. Penanganan Validasi Input
Saat form disubmit, `event.preventDefault()` mencegah reload halaman. Fungsi `validasiForm()` memanggil `validasiNama()`, `validasiHarga()`, dan `validasiQty()`. Masing-masing mengembalikan teks pesan error (atau string kosong jika valid). Pesan ditampilkan lewat elemen `<small class="error">` berwarna merah di bawah input, dan input diberi class `invalid`. Jika ada satu saja yang tidak valid, fungsi berhenti (`return`) sehingga barang tidak ditambahkan. Jika semua valid, barang dimasukkan ke array `keranjang` dan form di-reset dengan `formBarang.reset()`.

### 2. Algoritma Kalkulator
- **Subtotal** = `harga × qty` (`hitungSubtotal()`).
- **Total belanja** dihitung dengan `reduce()` yang menjumlahkan seluruh subtotal (`hitungTotalBelanja()`).
- **Diskon** 10% diberikan jika total ≥ Rp 50.000 atau kode promo `HEMAT10` diisi (`hitungDiskon()`). Diskon tidak ditumpuk.
- **Total akhir** = total belanja − diskon.
- **Kembalian** = uang bayar − total akhir (`hitungKembalian()`). Jika negatif, ditampilkan keterangan uang belum mencukupi beserta kekurangannya.
- Semua perhitungan dijalankan ulang oleh `perbaruiRingkasan()` setiap keranjang, kode promo, atau uang bayar berubah.

### 3. Mekanisme Serialisasi localStorage
- Keranjang berupa array of object `{ nama, harga, qty }`.
- `simpanKeranjang()` mengubah array menjadi string dengan `JSON.stringify(keranjang)` lalu menyimpannya ke `localStorage` dengan key `miniPosKeranjang`. Fungsi ini dipanggil setiap barang ditambah atau dihapus.
- `muatKeranjang()` dipanggil saat halaman dibuka. Fungsi ini membaca data dengan `localStorage.getItem()` lalu mengubahnya kembali menjadi array dengan `JSON.parse()`, sehingga isi keranjang tetap ada setelah di-refresh.
- Tombol reset memanggil `localStorage.removeItem()` untuk membersihkan data.

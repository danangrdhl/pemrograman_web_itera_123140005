"""Program Utama Demonstrasi Penggunaan Modul math_operations.

Tugas 3 Praktikum Pemrograman Web - Python Dasar
Nama : Danang
NIM  : 123140005

Program ini menguji seluruh fungsi pada modul math_operations
dengan menerapkan minimal 2 cara import yang berbeda:
1. import math_operations
2. from math_operations import ...
"""

# Cara Import 1: Mengimpor modul secara utuh
import math_operations

# Cara Import 2: Mengimpor fungsi dan konstanta tertentu secara langsung
from math_operations import (
    PI,
    celsius_ke_fahrenheit,
    celsius_ke_kelvin,
    keliling_lingkaran,
    luas_lingkaran,
)


def demo_geometri() -> None:
    """Menguji dan menampilkan kalkulasi bangun datar geometri."""
    print("=" * 60)
    print("              DEMONSTRASI PERHITUNGAN GEOMETRI              ")
    print("=" * 60)

    # 1. Persegi (dipanggil melalui modul math_operations)
    sisi = 7.0
    luas_p = math_operations.luas_persegi(sisi)
    kel_p = math_operations.keliling_persegi(sisi)

    print(f"[1] Persegi (Sisi = {sisi} cm)")
    print(f"    - Cara Panggilan: math_operations.luas_persegi()")
    print(f"    - Luas          : {luas_p:.2f} cm²")
    print(f"    - Keliling      : {kel_p:.2f} cm")
    print("-" * 60)

    # 2. Persegi Panjang (dipanggil melalui modul math_operations)
    panjang = 12.0
    lebar = 5.0
    luas_pp = math_operations.luas_persegi_panjang(panjang, lebar)
    kel_pp = math_operations.keliling_persegi_panjang(panjang, lebar)

    print(f"[2] Persegi Panjang (Panjang = {panjang} cm, Lebar = {lebar} cm)")
    print(f"    - Cara Panggilan: math_operations.luas_persegi_panjang()")
    print(f"    - Luas          : {luas_pp:.2f} cm²")
    print(f"    - Keliling      : {kel_pp:.2f} cm")
    print("-" * 60)

    # 3. Lingkaran (dipanggil langsung via from math_operations import ...)
    jari_jari = 10.0
    luas_l = luas_lingkaran(jari_jari)
    kel_l = keliling_lingkaran(jari_jari)

    print(f"[3] Lingkaran (Jari-jari = {jari_jari} cm, PI = {PI})")
    print(f"    - Cara Panggilan: luas_lingkaran() [direct import]")
    print(f"    - Luas          : {luas_l:.2f} cm²")
    print(f"    - Keliling      : {kel_l:.2f} cm")
    print("=" * 60)


def demo_konversi_suhu() -> None:
    """Menguji dan menampilkan konversi temperatur suhu."""
    print("\n" + "=" * 60)
    print("            DEMONSTRASI KONVERSI TEMPERATUR SUHU            ")
    print("=" * 60)
    print(f"Menggunakan direct import: celsius_ke_fahrenheit, celsius_ke_kelvin\n")

    daftar_suhu_celsius = [0.0, 25.0, 36.5, 100.0]

    print(f"| {'Celsius (°C)':^14} | {'Fahrenheit (°F)':^18} | {'Kelvin (K)':^16} |")
    print("|" + "-" * 16 + "|" + "-" * 20 + "|" + "-" * 18 + "|")

    for c in daftar_suhu_celsius:
        f = celsius_ke_fahrenheit(c)
        k = celsius_ke_kelvin(c)
        print(f"| {c:>12.2f} °C | {f:>16.2f} °F | {k:>14.2f} K  |")

    print("=" * 60)


def main() -> None:
    """Fungsi utama program demonstrasi."""
    print("=" * 60)
    print(" PRAKTIKUM PEMROGRAMAN WEB - TUGAS 3: MODUL PYTHON")
    print(" Identitas Mahasiswa: Danang (NIM: 123140005)")
    print("=" * 60)
    print("Metode Import yang Digunakan:")
    print(" 1. import math_operations")
    print(" 2. from math_operations import PI, celsius_ke_fahrenheit, ...")
    print()

    demo_geometri()
    demo_konversi_suhu()


if __name__ == "__main__":
    main()

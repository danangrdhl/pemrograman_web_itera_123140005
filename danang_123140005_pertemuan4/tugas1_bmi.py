"""Program Penghitung BMI (Body Mass Index) Sederhana.

Tugas 1 Praktikum Pemrograman Web - Python Dasar
Nama : Danang
NIM  : 123140005
"""


def hitung_bmi(berat: float, tinggi: float) -> float:
    """Menghitung nilai Body Mass Index (BMI).

    Parameter:
        berat (float): Berat badan dalam satuan kilogram (kg).
        tinggi (float): Tinggi badan dalam satuan meter (m).

    Returns:
        float: Nilai BMI yang dihitung dengan rumus berat / (tinggi * tinggi).
    """
    return berat / (tinggi * tinggi)


def tentukan_kategori_bmi(bmi: float) -> str:
    """Menentukan kategori status berat badan berdasarkan nilai BMI.

    Kriteria:
        - BMI < 18.5       : Berat badan kurang
        - 18.5 <= BMI < 25 : Berat badan normal
        - 25 <= BMI < 30   : Berat badan berlebih
        - BMI >= 30        : Obesitas

    Parameter:
        bmi (float): Nilai BMI.

    Returns:
        str: Kategori berat badan.
    """
    if bmi < 18.5:
        return "Berat badan kurang"
    elif bmi < 25.0:
        return "Berat badan normal"
    elif bmi < 30.0:
        return "Berat badan berlebih"
    else:
        return "Obesitas"


def main() -> None:
    """Fungsi utama untuk menjalankan program perhitungan BMI."""
    print("=" * 45)
    print("      PROGRAM PENGHITUNG BMI SEDERHANA       ")
    print("=" * 45)

    try:
        input_berat = input("Masukkan berat badan Anda (kg) : ").strip()
        input_tinggi = input("Masukkan tinggi badan Anda (m)  : ").strip()

        berat = float(input_berat)
        tinggi = float(input_tinggi)

        if berat <= 0 or tinggi <= 0:
            print("\n[Error] Berat dan tinggi badan harus bernilai positif (> 0).")
            return

        bmi = hitung_bmi(berat, tinggi)
        kategori = tentukan_kategori_bmi(bmi)

        print("-" * 45)
        print("HASIL PERHITUNGAN BMI:")
        print(f"Berat Badan    : {berat:.2f} kg")
        print(f"Tinggi Badan   : {tinggi:.2f} m")
        print(f"Nilai BMI      : {bmi:.2f}")
        print(f"Kategori Status: {kategori}")
        print("=" * 45)

    except ValueError:
        print("\n[Error] Masukan tidak valid! Harap masukkan angka yang benar.")


if __name__ == "__main__":
    main()

"""Modul Operasi Matematika dan Konversi Suhu.

Tugas 3 Praktikum Pemrograman Web - Python Dasar
Modul ini menyediakan fungsi perhitungan geometri (luas & keliling)
serta fungsi konversi temperatur suhu.

Nama : Danang
NIM  : 123140005
"""

# Konstanta Nilai Pi
PI: float = 3.14159


# ============================================================================
# FUNGSI PERHITUNGAN GEOMETRI
# ============================================================================


def luas_persegi(sisi: float) -> float:
    """Menghitung luas bangun datar persegi.

    Rumus: sisi * sisi

    Parameter:
        sisi (float): Panjang sisi persegi.

    Returns:
        float: Luas persegi.
    """
    return sisi * sisi


def keliling_persegi(sisi: float) -> float:
    """Menghitung keliling bangun datar persegi.

    Rumus: 4 * sisi

    Parameter:
        sisi (float): Panjang sisi persegi.

    Returns:
        float: Keliling persegi.
    """
    return 4 * sisi


def luas_persegi_panjang(panjang: float, lebar: float) -> float:
    """Menghitung luas bangun datar persegi panjang.

    Rumus: panjang * lebar

    Parameter:
        panjang (float): Panjang persegi panjang.
        lebar (float): Lebar persegi panjang.

    Returns:
        float: Luas persegi panjang.
    """
    return panjang * lebar


def keliling_persegi_panjang(panjang: float, lebar: float) -> float:
    """Menghitung keliling bangun datar persegi panjang.

    Rumus: 2 * (panjang + lebar)

    Parameter:
        panjang (float): Panjang persegi panjang.
        lebar (float): Lebar persegi panjang.

    Returns:
        float: Keliling persegi panjang.
    """
    return 2 * (panjang + lebar)


def luas_lingkaran(jari_jari: float) -> float:
    """Menghitung luas bangun datar lingkaran.

    Rumus: PI * jari_jari * jari_jari

    Parameter:
        jari_jari (float): Jari-jari lingkaran.

    Returns:
        float: Luas lingkaran.
    """
    return PI * (jari_jari**2)


def keliling_lingkaran(jari_jari: float) -> float:
    """Menghitung keliling bangun datar lingkaran.

    Rumus: 2 * PI * jari_jari

    Parameter:
        jari_jari (float): Jari-jari lingkaran.

    Returns:
        float: Keliling lingkaran.
    """
    return 2 * PI * jari_jari


# ============================================================================
# FUNGSI KONVERSI TEMPERATUR SUHU
# ============================================================================


def celsius_ke_fahrenheit(celsius: float) -> float:
    """Mengonversi nilai temperatur dari Celsius ke Fahrenheit.

    Rumus: (celsius * 9/5) + 32

    Parameter:
        celsius (float): Suhu dalam derajat Celsius (°C).

    Returns:
        float: Suhu dalam derajat Fahrenheit (°F).
    """
    return (celsius * 9 / 5) + 32


def celsius_ke_kelvin(celsius: float) -> float:
    """Mengonversi nilai temperatur dari Celsius ke Kelvin.

    Rumus: celsius + 273.15

    Parameter:
        celsius (float): Suhu dalam derajat Celsius (°C).

    Returns:
        float: Suhu dalam Kelvin (K).
    """
    return celsius + 273.15

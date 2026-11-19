"""Program Pengelolaan Data Nilai Mahasiswa.

Tugas 2 Praktikum Pemrograman Web - Python Dasar
Nama : Danang
NIM  : 123140005
"""

from typing import Any, Dict, List, Tuple


def hitung_nilai_akhir(uts: float, uas: float, tugas: float) -> float:
    """Menghitung nilai akhir mahasiswa berdasarkan bobot persentase.

    Rumus: (30% * UTS) + (40% * UAS) + (30% * Tugas)

    Parameter:
        uts (float): Nilai Ujian Tengah Semester.
        uas (float): Nilai Ujian Akhir Semester.
        tugas (float): Nilai Tugas.

    Returns:
        float: Nilai akhir terhitung.
    """
    return (0.30 * uts) + (0.40 * uas) + (0.30 * tugas)


def tentukan_grade(nilai_akhir: float) -> str:
    """Menentukan grade huruf berdasarkan kriteria nilai akhir.

    Kriteria:
        - A : Nilai akhir >= 80
        - B : 70 <= Nilai akhir < 80
        - C : 60 <= Nilai akhir < 70
        - D : 50 <= Nilai akhir < 60
        - E : Nilai akhir < 50

    Parameter:
        nilai_akhir (float): Nilai akhir mahasiswa.

    Returns:
        str: Grade huruf (A, B, C, D, atau E).
    """
    if nilai_akhir >= 80.0:
        return "A"
    elif nilai_akhir >= 70.0:
        return "B"
    elif nilai_akhir >= 60.0:
        return "C"
    elif nilai_akhir >= 50.0:
        return "D"
    else:
        return "E"


def proses_data_mahasiswa(daftar_mhs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Memproses list data mahasiswa untuk menambahkan nilai akhir dan grade.

    Parameter:
        daftar_mhs (List[Dict[str, Any]]): List dictionary data mahasiswa asal.

    Returns:
        List[Dict[str, Any]]: List dictionary mahasiswa yang telah dilengkapi
                              nilai akhir dan grade.
    """
    hasil = []
    for mhs in daftar_mhs:
        mhs_copy = mhs.copy()
        na = hitung_nilai_akhir(
            mhs["nilai_uts"], mhs["nilai_uas"], mhs["nilai_tugas"]
        )
        grade = tentukan_grade(na)
        mhs_copy["nilai_akhir"] = na
        mhs_copy["grade"] = grade
        hasil.append(mhs_copy)
    return hasil


def cari_ekstrem_nilai(
    daftar_mhs: List[Dict[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Mencari data mahasiswa dengan nilai akhir tertinggi dan terendah.

    Parameter:
        daftar_mhs (List[Dict[str, Any]]): List mahasiswa dengan nilai_akhir.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]:
            (mahasiswa_tertinggi, mahasiswa_terendah)
    """
    tertinggi = max(daftar_mhs, key=lambda m: m["nilai_akhir"])
    terendah = min(daftar_mhs, key=lambda m: m["nilai_akhir"])
    return tertinggi, terendah


def cetak_tabel_mahasiswa(daftar_mhs: List[Dict[str, Any]]) -> None:
    """Mencetak data mahasiswa ke konsol dalam format tabel yang rapi.

    Parameter:
        daftar_mhs (List[Dict[str, Any]]): List data mahasiswa lengkap.
    """
    garis = "=" * 88
    garis_tipis = "-" * 88

    print(garis)
    print(f"{'DAFTAR NILAI AKHIR MAHASISWA':^88}")
    print(garis)
    print(
        f"| {'No':<3} | {'NIM':<12} | {'Nama Mahasiswa':<22} | "
        f"{'UTS':>5} | {'UAS':>5} | {'Tugas':>5} | {'Akhir':>6} | {'Grade':^5} |"
    )
    print(garis_tipis)

    for i, mhs in enumerate(daftar_mhs, start=1):
        print(
            f"| {i:<3} | {mhs['nim']:<12} | {mhs['nama']:<22} | "
            f"{mhs['nilai_uts']:>5.1f} | {mhs['nilai_uas']:>5.1f} | {mhs['nilai_tugas']:>5.1f} | "
            f"{mhs['nilai_akhir']:>6.2f} | {mhs['grade']:^5} |"
        )

    print(garis)


def main() -> None:
    """Fungsi utama untuk menjalankan program pengelolaan data mahasiswa."""
    # List minimal 5 dictionary data mahasiswa
    data_mahasiswa: List[Dict[str, Any]] = [
        {
            "nama": "Danang",
            "nim": "123140005",
            "nilai_uts": 85.0,
            "nilai_uas": 90.0,
            "nilai_tugas": 88.0,
        },
        {
            "nama": "Ahmad Fauzi",
            "nim": "123140012",
            "nilai_uts": 75.0,
            "nilai_uas": 78.0,
            "nilai_tugas": 80.0,
        },
        {
            "nama": "Siti Nurhaliza",
            "nim": "123140023",
            "nilai_uts": 65.0,
            "nilai_uas": 60.0,
            "nilai_tugas": 70.0,
        },
        {
            "nama": "Budi Santoso",
            "nim": "123140034",
            "nilai_uts": 52.0,
            "nilai_uas": 58.0,
            "nilai_tugas": 55.0,
        },
        {
            "nama": "Citra Lestari",
            "nim": "123140045",
            "nilai_uts": 40.0,
            "nilai_uas": 45.0,
            "nilai_tugas": 48.0,
        },
        {
            "nama": "Eko Prasetyo",
            "nim": "123140056",
            "nilai_uts": 92.0,
            "nilai_uas": 95.0,
            "nilai_tugas": 90.0,
        },
    ]

    # Proses perhitungan nilai akhir dan penentuan grade
    data_terproses = proses_data_mahasiswa(data_mahasiswa)

    # Tampilkan tabel data mahasiswa
    cetak_tabel_mahasiswa(data_terproses)

    # Temukan mahasiswa dengan nilai tertinggi dan terendah
    mhs_tertinggi, mhs_terendah = cari_ekstrem_nilai(data_terproses)

    print("\nRINGKASAN STATISTIK NILAI:")
    print("-" * 55)
    print("🏆 Mahasiswa Nilai Akhir TERTINGGI:")
    print(f"   Nama        : {mhs_tertinggi['nama']}")
    print(f"   NIM         : {mhs_tertinggi['nim']}")
    print(f"   Nilai Akhir : {mhs_tertinggi['nilai_akhir']:.2f} (Grade: {mhs_tertinggi['grade']})")
    print("-" * 55)
    print("⚠️ Mahasiswa Nilai Akhir TERENDAH:")
    print(f"   Nama        : {mhs_terendah['nama']}")
    print(f"   NIM         : {mhs_terendah['nim']}")
    print(f"   Nilai Akhir : {mhs_terendah['nilai_akhir']:.2f} (Grade: {mhs_terendah['grade']})")
    print("-" * 55)


if __name__ == "__main__":
    main()

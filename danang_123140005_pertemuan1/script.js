/* ==========================================================
   Mini POS - Kasir & Keranjang Belanja Sederhana
   ========================================================== */

// ---------- Konstanta ----------
const STORAGE_KEY = "miniPosKeranjang";
const MIN_NAMA = 3;
const MIN_HARGA = 500;
const MIN_QTY = 1;
const MIN_BELANJA_DISKON = 50000;
const PERSEN_DISKON = 10;
const KODE_PROMO = "HEMAT10";

// ---------- State ----------
let keranjang = [];

// ---------- Elemen DOM ----------
const formBarang = document.getElementById("form-barang");
const inputNama = document.getElementById("nama-barang");
const inputHarga = document.getElementById("harga-barang");
const inputQty = document.getElementById("qty-barang");
const errorNama = document.getElementById("error-nama");
const errorHarga = document.getElementById("error-harga");
const errorQty = document.getElementById("error-qty");

const isiKeranjang = document.getElementById("isi-keranjang");
const keranjangKosong = document.getElementById("keranjang-kosong");

const totalBelanjaEl = document.getElementById("total-belanja");
const inputKodePromo = document.getElementById("kode-promo");
const infoPromo = document.getElementById("info-promo");
const nominalDiskonEl = document.getElementById("nominal-diskon");
const totalAkhirEl = document.getElementById("total-akhir");
const inputUangBayar = document.getElementById("uang-bayar");
const kembalianEl = document.getElementById("kembalian");
const statusBayarEl = document.getElementById("status-bayar");
const btnReset = document.getElementById("btn-reset");

// ---------- Helper ----------
function formatRupiah(angka) {
  return "Rp " + Math.round(angka).toLocaleString("id-ID");
}

// ---------- LocalStorage ----------
function simpanKeranjang() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(keranjang));
}

function muatKeranjang() {
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
    keranjang = Array.isArray(data) ? data : [];
  } catch (error) {
    keranjang = [];
  }
}

// ---------- Validasi ----------
function tampilkanError(input, elemenError, pesan) {
  elemenError.textContent = pesan;
  input.classList.add("invalid");
}

function hapusError(input, elemenError) {
  elemenError.textContent = "";
  input.classList.remove("invalid");
}

function validasiNama(nama) {
  if (nama.length === 0) return "Nama barang wajib diisi.";
  if (nama.length < MIN_NAMA) return "Nama barang minimal " + MIN_NAMA + " karakter.";
  return "";
}

function validasiHarga(nilai) {
  if (nilai === "") return "Harga satuan wajib diisi.";
  const harga = Number(nilai);
  if (isNaN(harga)) return "Harga satuan harus berupa angka.";
  if (harga <= 0) return "Harga satuan harus berupa angka positif.";
  if (harga < MIN_HARGA) return "Harga satuan minimal Rp " + MIN_HARGA.toLocaleString("id-ID") + ".";
  return "";
}

function validasiQty(nilai) {
  if (nilai === "") return "Jumlah wajib diisi.";
  const qty = Number(nilai);
  if (isNaN(qty)) return "Jumlah harus berupa angka.";
  if (!Number.isInteger(qty)) return "Jumlah harus berupa bilangan bulat.";
  if (qty < MIN_QTY) return "Jumlah minimal " + MIN_QTY + ".";
  return "";
}

function validasiForm() {
  const pesanNama = validasiNama(inputNama.value.trim());
  const pesanHarga = validasiHarga(inputHarga.value.trim());
  const pesanQty = validasiQty(inputQty.value.trim());

  pesanNama ? tampilkanError(inputNama, errorNama, pesanNama) : hapusError(inputNama, errorNama);
  pesanHarga ? tampilkanError(inputHarga, errorHarga, pesanHarga) : hapusError(inputHarga, errorHarga);
  pesanQty ? tampilkanError(inputQty, errorQty, pesanQty) : hapusError(inputQty, errorQty);

  return !pesanNama && !pesanHarga && !pesanQty;
}

// ---------- Perhitungan ----------
function hitungSubtotal(item) {
  return item.harga * item.qty;
}

function hitungTotalBelanja() {
  return keranjang.reduce((total, item) => total + hitungSubtotal(item), 0);
}

function hitungDiskon(total) {
  const kode = inputKodePromo.value.trim().toUpperCase();
  const pakaiKode = kode === KODE_PROMO;
  const memenuhiMinimal = total >= MIN_BELANJA_DISKON;

  if (total > 0 && (memenuhiMinimal || pakaiKode)) {
    return total * (PERSEN_DISKON / 100);
  }
  return 0;
}

function perbaruiInfoPromo(total) {
  const kode = inputKodePromo.value.trim().toUpperCase();
  infoPromo.className = "info";

  if (kode === "") {
    infoPromo.textContent = "Diskon 10% otomatis jika total belanja ≥ Rp 50.000.";
  } else if (kode === KODE_PROMO) {
    infoPromo.textContent = "Kode promo HEMAT10 berhasil dipakai (diskon 10%).";
    infoPromo.classList.add("sukses");
  } else {
    infoPromo.textContent = "Kode promo tidak valid.";
    infoPromo.classList.add("gagal");
  }
}

function hitungKembalian(totalAkhir) {
  const nilai = inputUangBayar.value.trim();
  statusBayarEl.className = "status";

  if (nilai === "" || totalAkhir <= 0) {
    kembalianEl.textContent = formatRupiah(0);
    statusBayarEl.textContent = "";
    return;
  }

  const uangBayar = Number(nilai);
  const kembalian = uangBayar - totalAkhir;

  if (kembalian < 0) {
    kembalianEl.textContent = formatRupiah(0);
    statusBayarEl.textContent =
      "Uang belum mencukupi, kurang " + formatRupiah(Math.abs(kembalian)) + ".";
    statusBayarEl.classList.add("kurang");
  } else {
    kembalianEl.textContent = formatRupiah(kembalian);
    statusBayarEl.textContent = "Pembayaran mencukupi.";
    statusBayarEl.classList.add("cukup");
  }
}

function perbaruiRingkasan() {
  const total = hitungTotalBelanja();
  const diskon = hitungDiskon(total);
  const totalAkhir = total - diskon;

  totalBelanjaEl.textContent = formatRupiah(total);
  nominalDiskonEl.textContent = "- " + formatRupiah(diskon);
  totalAkhirEl.textContent = formatRupiah(totalAkhir);

  perbaruiInfoPromo(total);
  hitungKembalian(totalAkhir);
}

// ---------- Render tabel ----------
function buatSel(teks, kelas) {
  const td = document.createElement("td");
  td.textContent = teks;
  if (kelas) td.className = kelas;
  return td;
}

function renderKeranjang() {
  isiKeranjang.innerHTML = "";

  keranjang.forEach((item, index) => {
    const tr = document.createElement("tr");

    tr.appendChild(buatSel(index + 1));
    tr.appendChild(buatSel(item.nama));
    tr.appendChild(buatSel(formatRupiah(item.harga), "right"));
    tr.appendChild(buatSel(item.qty, "center"));
    tr.appendChild(buatSel(formatRupiah(hitungSubtotal(item)), "right"));

    const tdAksi = document.createElement("td");
    tdAksi.className = "center";
    const btnHapus = document.createElement("button");
    btnHapus.type = "button";
    btnHapus.className = "btn btn-hapus";
    btnHapus.textContent = "Hapus";
    btnHapus.dataset.index = index;
    tdAksi.appendChild(btnHapus);
    tr.appendChild(tdAksi);

    isiKeranjang.appendChild(tr);
  });

  keranjangKosong.style.display = keranjang.length === 0 ? "block" : "none";
  perbaruiRingkasan();
}

// ---------- Aksi ----------
function tambahBarang(event) {
  event.preventDefault();

  if (!validasiForm()) return; // barang tidak masuk keranjang jika tidak valid

  keranjang.push({
    nama: inputNama.value.trim(),
    harga: Number(inputHarga.value),
    qty: Number(inputQty.value),
  });

  simpanKeranjang();
  renderKeranjang();

  formBarang.reset(); // reset form setelah berhasil
  hapusError(inputNama, errorNama);
  hapusError(inputHarga, errorHarga);
  hapusError(inputQty, errorQty);
  inputNama.focus();
}

function hapusBarang(index) {
  keranjang.splice(index, 1);
  simpanKeranjang();
  renderKeranjang();
}

function resetTransaksi() {
  if (keranjang.length > 0 && !confirm("Kosongkan keranjang dan mulai transaksi baru?")) {
    return;
  }
  keranjang = [];
  localStorage.removeItem(STORAGE_KEY);
  inputKodePromo.value = "";
  inputUangBayar.value = "";
  renderKeranjang();
}

// ---------- Event listener ----------
formBarang.addEventListener("submit", tambahBarang);

isiKeranjang.addEventListener("click", function (event) {
  const tombol = event.target.closest(".btn-hapus");
  if (tombol) hapusBarang(Number(tombol.dataset.index));
});

inputKodePromo.addEventListener("input", perbaruiRingkasan);
inputUangBayar.addEventListener("input", perbaruiRingkasan);
btnReset.addEventListener("click", resetTransaksi);

// Hapus pesan error saat pengguna mulai mengetik ulang
inputNama.addEventListener("input", () => hapusError(inputNama, errorNama));
inputHarga.addEventListener("input", () => hapusError(inputHarga, errorHarga));
inputQty.addEventListener("input", () => hapusError(inputQty, errorQty));

// ---------- Inisialisasi ----------
muatKeranjang();
renderKeranjang();

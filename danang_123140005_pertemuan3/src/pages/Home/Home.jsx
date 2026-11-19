import { useState } from 'react';
import { useBooks } from '../../context/BookContext';
import { useBookStats } from '../../hooks/useBookStats';
import { BookFilter } from '../../components/BookFilter/BookFilter';
import { BookList } from '../../components/BookList/BookList';
import { BookForm } from '../../components/BookForm/BookForm';
import { ConfirmDialog } from '../../components/ConfirmDialog/ConfirmDialog';
import './Home.css';

export function Home() {
  const {
    books,
    filteredBooks,
    filterStatus,
    setFilterStatus,
    searchQuery,
    setSearchQuery,
    editingBook,
    isFormOpen,
    addBook,
    updateBook,
    deleteBook,
    openAddModal,
    openEditModal,
    closeFormModal,
  } = useBooks();

  // Hitung ringkasan statistik untuk filter counter
  const stats = useBookStats(books);

  // State untuk dialog konfirmasi hapus
  const [deleteCandidate, setDeleteCandidate] = useState(null);

  // State notifikasi toast
  const [toastMessage, setToastMessage] = useState('');

  const showToast = (message) => {
    setToastMessage(message);
    setTimeout(() => {
      setToastMessage('');
    }, 3000);
  };

  // Handler simpan form (tambah atau edit)
  const handleFormSubmit = (formData) => {
    if (editingBook) {
      updateBook(editingBook.id, formData);
      showToast(`Buku "${formData.title}" berhasil diperbarui.`);
    } else {
      addBook(formData);
      showToast(`Buku "${formData.title}" berhasil ditambahkan ke koleksi.`);
    }
  };

  // Handler memicu dialog hapus
  const handleDeletePrompt = (id, title) => {
    setDeleteCandidate({ id, title });
  };

  // Konfirmasi eksekusi hapus
  const handleConfirmDelete = () => {
    if (deleteCandidate) {
      deleteBook(deleteCandidate.id);
      showToast(`Buku "${deleteCandidate.title}" telah dihapus.`);
      setDeleteCandidate(null);
    }
  };

  return (
    <div className="home-page">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="toast" role="status" aria-live="polite">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Hero / Header Section */}
      <section className="home-hero">
        <div className="home-hero-text">
          <h1 className="home-title">Koleksi Buku Pribadi</h1>
          <p className="home-subtitle">
            Kelola buku yang Anda miliki, sedang dibaca, atau yang ada di daftar keinginan belanja Anda.
          </p>
        </div>
        <button
          type="button"
          className="btn btn-primary btn-add-main"
          onClick={openAddModal}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          Tambah Buku Baru
        </button>
      </section>

      {/* Quick Summary Cards */}
      <div className="quick-stats-row">
        <div className="quick-stat-card">
          <span className="stat-label">Total Buku</span>
          <span className="stat-value">{stats.total}</span>
        </div>
        <div className="quick-stat-card border-milik">
          <span className="stat-label">Dimiliki</span>
          <span className="stat-value">{stats.milik}</span>
        </div>
        <div className="quick-stat-card border-baca">
          <span className="stat-label">Sedang Dibaca</span>
          <span className="stat-value">{stats.baca}</span>
        </div>
        <div className="quick-stat-card border-beli">
          <span className="stat-label">Ingin Dibeli</span>
          <span className="stat-value">{stats.beli}</span>
        </div>
      </div>

      {/* Komponen Filter & Search Reusable */}
      <BookFilter
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        filterStatus={filterStatus}
        onFilterChange={setFilterStatus}
        counts={{
          total: stats.total,
          milik: stats.milik,
          baca: stats.baca,
          beli: stats.beli,
        }}
      />

      {/* Komponen BookList Reusable */}
      <BookList
        books={filteredBooks}
        onEdit={openEditModal}
        onDelete={handleDeletePrompt}
        onAddNew={openAddModal}
      />

      {/* Modal Form Reusable (Tambah / Edit) */}
      <BookForm
        isOpen={isFormOpen}
        onClose={closeFormModal}
        onSubmit={handleFormSubmit}
        initialData={editingBook}
      />

      {/* Dialog Konfirmasi Hapus Reusable */}
      <ConfirmDialog
        isOpen={Boolean(deleteCandidate)}
        title="Hapus Buku"
        message={`Apakah Anda yakin ingin menghapus buku "${deleteCandidate?.title}" dari koleksi? Tindakan ini tidak dapat dibatalkan.`}
        confirmText="Hapus Buku"
        cancelText="Batal"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteCandidate(null)}
      />
    </div>
  );
}

export default Home;

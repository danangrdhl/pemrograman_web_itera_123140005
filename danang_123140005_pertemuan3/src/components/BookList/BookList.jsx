import PropTypes from 'prop-types';
import './BookList.css';

/**
 * Komponen reusable untuk menampilkan daftar buku dalam bentuk kartu responsif
 */
export function BookList({ books, onEdit, onDelete, onAddNew = null }) {
  if (!books || books.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            <line x1="9" y1="9" x2="15" y2="9" />
          </svg>
        </div>
        <h3 className="empty-title">Belum Ada Buku Ditemukan</h3>
        <p className="empty-description">
          Tidak ada buku yang sesuai dengan filter atau pencarian Anda. Coba kata kunci lain atau tambahkan buku baru ke koleksi.
        </p>
        {onAddNew && (
          <button type="button" className="btn btn-primary" onClick={onAddNew}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Tambah Buku Sekarang
          </button>
        )}
      </div>
    );
  }

  // Label dan style status
  const statusMeta = {
    milik: { label: 'Dimiliki', class: 'badge-milik' },
    baca: { label: 'Sedang Dibaca', class: 'badge-baca' },
    beli: { label: 'Ingin Dibeli', class: 'badge-beli' },
  };

  return (
    <div className="book-grid" role="list">
      {books.map((book) => {
        const meta = statusMeta[book.status] || {
          label: book.status,
          class: 'badge-milik',
        };

        return (
          <article key={book.id} className="book-card" role="listitem">
            <div className="book-card-header">
              <span className={`badge ${meta.class}`}>
                <span className="badge-dot" />
                {meta.label}
              </span>
              <div className="book-actions">
                <button
                  type="button"
                  className="icon-btn icon-btn-edit"
                  onClick={() => onEdit(book)}
                  title="Edit Buku"
                  aria-label={`Edit ${book.title}`}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                  </svg>
                </button>
                <button
                  type="button"
                  className="icon-btn icon-btn-delete"
                  onClick={() => onDelete(book.id, book.title)}
                  title="Hapus Buku"
                  aria-label={`Hapus ${book.title}`}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="3 6 5 6 21 6" />
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                    <line x1="10" y1="11" x2="10" y2="17" />
                    <line x1="14" y1="11" x2="14" y2="17" />
                  </svg>
                </button>
              </div>
            </div>

            <div className="book-card-body">
              <h3 className="book-title" title={book.title}>
                {book.title}
              </h3>
              <p className="book-author">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                <span>{book.author}</span>
              </p>
            </div>

            {book.createdAt && (
              <div className="book-card-footer">
                <small className="book-date">
                  Ditambahkan:{' '}
                  {new Date(book.createdAt).toLocaleDateString('id-ID', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                  })}
                </small>
              </div>
            )}
          </article>
        );
      })}
    </div>
  );
}

BookList.propTypes = {
  books: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      author: PropTypes.string.isRequired,
      status: PropTypes.oneOf(['milik', 'baca', 'beli']).isRequired,
      createdAt: PropTypes.string,
    })
  ).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onAddNew: PropTypes.func,
};

export default BookList;

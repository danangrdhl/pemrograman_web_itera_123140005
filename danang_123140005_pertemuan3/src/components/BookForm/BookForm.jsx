import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './BookForm.css';

/**
 * Komponen modal form reusable untuk menambah dan mengedit buku
 * Dilengkapi dengan validasi kolom wajib isi dan feedback visual
 */
export function BookForm({ isOpen, onClose, onSubmit, initialData = null }) {
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    status: 'milik',
  });

  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  // Sinkronkan state form jika initialData berubah (saat edit)
  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title || '',
        author: initialData.author || '',
        status: initialData.status || 'milik',
      });
    } else {
      setFormData({
        title: '',
        author: '',
        status: 'milik',
      });
    }
    setErrors({});
    setTouched({});
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  // Validasi form
  const validate = (values) => {
    const errs = {};
    if (!values.title || !values.title.trim()) {
      errs.title = 'Judul buku wajib diisi';
    } else if (values.title.trim().length < 2) {
      errs.title = 'Judul buku minimal 2 karakter';
    }

    if (!values.author || !values.author.trim()) {
      errs.author = 'Nama penulis wajib diisi';
    } else if (values.author.trim().length < 2) {
      errs.author = 'Nama penulis minimal 2 karakter';
    }

    if (!['milik', 'baca', 'beli'].includes(values.status)) {
      errs.status = 'Status buku tidak valid';
    }

    return errs;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newFormData = { ...formData, [name]: value };
    setFormData(newFormData);

    // Jika kolom sudah pernah disentuh, perbarui validasi secara live
    if (touched[name]) {
      const validationErrors = validate(newFormData);
      setErrors((prev) => ({
        ...prev,
        [name]: validationErrors[name] || '',
      }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
    const validationErrors = validate(formData);
    setErrors((prev) => ({
      ...prev,
      [name]: validationErrors[name] || '',
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Tandai semua field sebagai touched
    setTouched({ title: true, author: true, status: true });

    const validationErrors = validate(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Panggil callback submit jika valid
    onSubmit(formData);
    onClose();
  };

  const isEditing = Boolean(initialData && initialData.id);

  return (
    <div className="modal-backdrop" onClick={onClose} role="dialog" aria-modal="true">
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-group">
            <h2 className="modal-title">
              {isEditing ? 'Edit Data Buku' : 'Tambah Buku Baru'}
            </h2>
            <p className="modal-subtitle">
              {isEditing
                ? 'Perbarui informasi judul, penulis, atau status buku Anda'
                : 'Catat buku ke dalam koleksi pribadi Anda'}
            </p>
          </div>
          <button
            type="button"
            className="modal-close-btn"
            onClick={onClose}
            aria-label="Tutup form"
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} className="book-form" noValidate>
          {/* Input Judul */}
          <div className="form-group">
            <label htmlFor="book-title" className="form-label">
              Judul Buku <span className="required-star">*</span>
            </label>
            <input
              id="book-title"
              name="title"
              type="text"
              className={`form-input ${errors.title ? 'input-error' : ''}`}
              placeholder="Contoh: Filosofi Teras"
              value={formData.title}
              onChange={handleChange}
              onBlur={handleBlur}
              aria-invalid={Boolean(errors.title)}
              aria-describedby={errors.title ? 'title-error' : undefined}
            />
            {errors.title && (
              <span id="title-error" className="error-feedback" role="alert">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                {errors.title}
              </span>
            )}
          </div>

          {/* Input Penulis */}
          <div className="form-group">
            <label htmlFor="book-author" className="form-label">
              Nama Penulis <span className="required-star">*</span>
            </label>
            <input
              id="book-author"
              name="author"
              type="text"
              className={`form-input ${errors.author ? 'input-error' : ''}`}
              placeholder="Contoh: Henry Manampiring"
              value={formData.author}
              onChange={handleChange}
              onBlur={handleBlur}
              aria-invalid={Boolean(errors.author)}
              aria-describedby={errors.author ? 'author-error' : undefined}
            />
            {errors.author && (
              <span id="author-error" className="error-feedback" role="alert">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                {errors.author}
              </span>
            )}
          </div>

          {/* Pilihan Status */}
          <div className="form-group">
            <label htmlFor="book-status" className="form-label">
              Status Buku <span className="required-star">*</span>
            </label>
            <div className="status-selector">
              <label className={`status-option ${formData.status === 'milik' ? 'status-option-active' : ''}`}>
                <input
                  type="radio"
                  name="status"
                  value="milik"
                  checked={formData.status === 'milik'}
                  onChange={handleChange}
                />
                <span className="status-label">
                  <span className="badge-dot" style={{ backgroundColor: '#4f46e5' }} />
                  Dimiliki
                </span>
              </label>

              <label className={`status-option ${formData.status === 'baca' ? 'status-option-active' : ''}`}>
                <input
                  type="radio"
                  name="status"
                  value="baca"
                  checked={formData.status === 'baca'}
                  onChange={handleChange}
                />
                <span className="status-label">
                  <span className="badge-dot" style={{ backgroundColor: '#d97706' }} />
                  Sedang Dibaca
                </span>
              </label>

              <label className={`status-option ${formData.status === 'beli' ? 'status-option-active' : ''}`}>
                <input
                  type="radio"
                  name="status"
                  value="beli"
                  checked={formData.status === 'beli'}
                  onChange={handleChange}
                />
                <span className="status-label">
                  <span className="badge-dot" style={{ backgroundColor: '#059669' }} />
                  Ingin Dibeli
                </span>
              </label>
            </div>
          </div>

          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
            >
              Batal
            </button>
            <button type="submit" className="btn btn-primary">
              {isEditing ? 'Simpan Perubahan' : 'Tambah Buku'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

BookForm.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  initialData: PropTypes.shape({
    id: PropTypes.string,
    title: PropTypes.string,
    author: PropTypes.string,
    status: PropTypes.oneOf(['milik', 'baca', 'beli']),
  }),
};

export default BookForm;

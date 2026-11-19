import PropTypes from 'prop-types';
import './ConfirmDialog.css';

/**
 * Komponen modal dialog konfirmasi yang dapat digunakan kembali (reusable)
 */
export function ConfirmDialog({
  isOpen,
  title = 'Konfirmasi Penghapusan',
  message,
  confirmText = 'Ya, Hapus',
  cancelText = 'Batal',
  onConfirm,
  onCancel,
}) {
  if (!isOpen) return null;

  return (
    <div className="confirm-backdrop" onClick={onCancel} role="dialog" aria-modal="true">
      <div className="confirm-modal" onClick={(e) => e.stopPropagation()}>
        <div className="confirm-icon-danger">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
        </div>

        <h3 className="confirm-title">{title}</h3>
        <p className="confirm-message">{message}</p>

        <div className="confirm-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
          >
            {cancelText}
          </button>
          <button
            type="button"
            className="btn btn-danger"
            onClick={onConfirm}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}

ConfirmDialog.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  title: PropTypes.string,
  message: PropTypes.string.isRequired,
  confirmText: PropTypes.string,
  cancelText: PropTypes.string,
  onConfirm: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};

export default ConfirmDialog;

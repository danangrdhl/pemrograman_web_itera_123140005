import PropTypes from 'prop-types';
import './BookFilter.css';

/**
 * Komponen reusable untuk pencarian dan pemfilteran buku berdasarkan status
 */
export function BookFilter({
  searchQuery,
  onSearchChange,
  filterStatus,
  onFilterChange,
  counts = { total: 0, milik: 0, baca: 0, beli: 0 },
}) {
  const filterOptions = [
    { key: 'semua', label: 'Semua', count: counts.total },
    { key: 'milik', label: 'Dimiliki', count: counts.milik },
    { key: 'baca', label: 'Sedang Dibaca', count: counts.baca },
    { key: 'beli', label: 'Ingin Dibeli', count: counts.beli },
  ];

  return (
    <div className="book-filter-container">
      {/* Input Pencarian */}
      <div className="search-bar">
        <span className="search-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        </span>
        <input
          type="text"
          className="search-input"
          placeholder="Cari buku berdasarkan judul atau nama penulis..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          aria-label="Cari buku"
        />
        {searchQuery && (
          <button
            type="button"
            className="search-clear-btn"
            onClick={() => onSearchChange('')}
            aria-label="Bersihkan pencarian"
          >
            &times;
          </button>
        )}
      </div>

      {/* Filter Tabs / Pills */}
      <div className="filter-tabs" role="tablist" aria-label="Filter status buku">
        {filterOptions.map((opt) => {
          const isActive = filterStatus === opt.key;
          return (
            <button
              key={opt.key}
              type="button"
              role="tab"
              aria-selected={isActive}
              className={`filter-tab ${isActive ? 'filter-tab-active' : ''}`}
              onClick={() => onFilterChange(opt.key)}
            >
              <span>{opt.label}</span>
              {typeof opt.count === 'number' && (
                <span className={`tab-counter ${isActive ? 'tab-counter-active' : ''}`}>
                  {opt.count}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}

BookFilter.propTypes = {
  searchQuery: PropTypes.string.isRequired,
  onSearchChange: PropTypes.func.isRequired,
  filterStatus: PropTypes.oneOf(['semua', 'milik', 'baca', 'beli']).isRequired,
  onFilterChange: PropTypes.func.isRequired,
  counts: PropTypes.shape({
    total: PropTypes.number,
    milik: PropTypes.number,
    baca: PropTypes.number,
    beli: PropTypes.number,
  }),
};

export default BookFilter;

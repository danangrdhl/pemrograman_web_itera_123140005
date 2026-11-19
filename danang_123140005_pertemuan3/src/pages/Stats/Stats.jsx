import { Link } from 'react-router-dom';
import { useBooks } from '../../context/BookContext';
import { useBookStats } from '../../hooks/useBookStats';
import './Stats.css';

export function Stats() {
  const { books } = useBooks();
  const stats = useBookStats(books);

  return (
    <div className="stats-page">
      <div className="stats-header">
        <div>
          <h1 className="stats-title">Statistik Koleksi Buku</h1>
          <p className="stats-subtitle">
            Wawasan analitik mengenai status membaca, kepemilikan, dan penulis di perpustakaan Anda.
          </p>
        </div>
        <Link to="/" className="btn btn-secondary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
          Kembali ke Koleksi
        </Link>
      </div>

      {/* Main KPI Cards */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon kpi-icon-total">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
          </div>
          <div className="kpi-content">
            <span className="kpi-label">Total Semua Buku</span>
            <span className="kpi-value">{stats.total}</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon kpi-icon-authors">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
          </div>
          <div className="kpi-content">
            <span className="kpi-label">Penulis Unik</span>
            <span className="kpi-value">{stats.uniqueAuthors}</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon kpi-icon-read">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
            </svg>
          </div>
          <div className="kpi-content">
            <span className="kpi-label">Sedang Dibaca</span>
            <span className="kpi-value">{stats.baca}</span>
          </div>
        </div>
      </div>

      {/* Detail Analytics Grid */}
      <div className="analytics-grid">
        {/* Distribusi Status */}
        <div className="analytics-card">
          <h2 className="card-heading">Distribusi Status Koleksi</h2>
          <p className="card-subtext">Persentase buku berdasarkan status saat ini.</p>

          <div className="progress-group">
            <div className="progress-header">
              <div className="progress-label">
                <span className="status-dot dot-milik" />
                <span>Buku Dimiliki</span>
              </div>
              <span className="progress-percentage">
                {stats.milik} ({stats.milikPercent}%)
              </span>
            </div>
            <div className="progress-track">
              <div
                className="progress-fill fill-milik"
                style={{ width: `${stats.milikPercent}%` }}
              />
            </div>
          </div>

          <div className="progress-group">
            <div className="progress-header">
              <div className="progress-label">
                <span className="status-dot dot-baca" />
                <span>Sedang Dibaca</span>
              </div>
              <span className="progress-percentage">
                {stats.baca} ({stats.bacaPercent}%)
              </span>
            </div>
            <div className="progress-track">
              <div
                className="progress-fill fill-baca"
                style={{ width: `${stats.bacaPercent}%` }}
              />
            </div>
          </div>

          <div className="progress-group">
            <div className="progress-header">
              <div className="progress-label">
                <span className="status-dot dot-beli" />
                <span>Ingin Dibeli (Wishlist)</span>
              </div>
              <span className="progress-percentage">
                {stats.beli} ({stats.beliPercent}%)
              </span>
            </div>
            <div className="progress-track">
              <div
                className="progress-fill fill-beli"
                style={{ width: `${stats.beliPercent}%` }}
              />
            </div>
          </div>
        </div>

        {/* Penulis Terbanyak */}
        <div className="analytics-card">
          <h2 className="card-heading">Penulis Terbanyak</h2>
          <p className="card-subtext">Penulis dengan karya terbanyak di perpustakaan Anda.</p>

          {stats.topAuthors.length === 0 ? (
            <p className="empty-subtext">Belum ada data penulis yang tersedia.</p>
          ) : (
            <ul className="authors-list">
              {stats.topAuthors.map((author, index) => (
                <li key={author.name} className="author-item">
                  <div className="author-rank">{index + 1}</div>
                  <div className="author-info">
                    <span className="author-name">{author.name}</span>
                    <span className="author-count">{author.count} Buku</span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default Stats;

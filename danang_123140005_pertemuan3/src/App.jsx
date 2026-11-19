import { Routes, Route } from 'react-router-dom';
import { BookProvider, useBooks } from './context/BookContext';
import { Navbar } from './components/Navbar/Navbar';
import { Home } from './pages/Home/Home';
import { Stats } from './pages/Stats/Stats';

// Konten utama dengan navigasi dan router
function AppContent() {
  const { openAddModal } = useBooks();

  return (
    <div className="app-container">
      {/* Header & Navigasi Reusable */}
      <Navbar onAddClick={openAddModal} />

      {/* Main Content Router */}
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>

      {/* Footer Aplikasi */}
      <footer
        style={{
          borderTop: '1px solid var(--border-color)',
          backgroundColor: '#ffffff',
          padding: '20px',
          textAlign: 'center',
          color: 'var(--text-secondary)',
          fontSize: '0.85rem',
        }}
      >
        <p>
          <strong>PustakaKu</strong> &copy; 2026 &bull; Tugas Praktikum PAW Pertemuan 3
        </p>
        <p style={{ marginTop: '4px', color: 'var(--text-muted)' }}>
          Danang Ridho Laksono &bull; NIM 123140005 &bull; Kelas RB
        </p>
      </footer>
    </div>
  );
}

export function App() {
  return (
    <BookProvider>
      <AppContent />
    </BookProvider>
  );
}

export default App;

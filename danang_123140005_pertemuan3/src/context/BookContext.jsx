import { createContext, useContext, useState, useMemo } from 'react';
import PropTypes from 'prop-types';
import { useLocalStorage } from '../hooks/useLocalStorage';

// Inisialisasi Context
export const BookContext = createContext(null);

// Data awal (seed data) jika localStorage masih kosong
const INITIAL_BOOKS = [
  {
    id: 'book-1',
    title: 'Laskar Pelangi',
    author: 'Andrea Hirata',
    status: 'milik',
    createdAt: new Date('2026-01-10').toISOString(),
  },
  {
    id: 'book-2',
    title: 'Filosofi Teras',
    author: 'Henry Manampiring',
    status: 'baca',
    createdAt: new Date('2026-02-15').toISOString(),
  },
  {
    id: 'book-3',
    title: 'Atomic Habits',
    author: 'James Clear',
    status: 'beli',
    createdAt: new Date('2026-03-01').toISOString(),
  },
  {
    id: 'book-4',
    title: 'Bumi Manusia',
    author: 'Pramoedya Ananta Toer',
    status: 'milik',
    createdAt: new Date('2026-03-20').toISOString(),
  },
];

/**
 * Provider untuk manajemen state buku secara global menggunakan Context API
 */
export function BookProvider({ children }) {
  // Simpan data buku ke localStorage dengan custom hook
  const [books, setBooks] = useLocalStorage('pustakaku_books', INITIAL_BOOKS);

  // State untuk filter dan pencarian
  const [filterStatus, setFilterStatus] = useState('semua');
  const [searchQuery, setSearchQuery] = useState('');

  // State untuk kontrol modal form dan buku yang sedang diedit
  const [editingBook, setEditingBook] = useState(null);
  const [isFormOpen, setIsFormOpen] = useState(false);

  // Fungsi menambah buku baru
  const addBook = (bookData) => {
    const newBook = {
      id: `book-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
      title: bookData.title.trim(),
      author: bookData.author.trim(),
      status: bookData.status,
      createdAt: new Date().toISOString(),
    };
    setBooks((prevBooks) => [newBook, ...prevBooks]);
  };

  // Fungsi memperbarui buku
  const updateBook = (id, updatedData) => {
    setBooks((prevBooks) =>
      prevBooks.map((book) =>
        book.id === id
          ? {
              ...book,
              title: updatedData.title.trim(),
              author: updatedData.author.trim(),
              status: updatedData.status,
              updatedAt: new Date().toISOString(),
            }
          : book
      )
    );
  };

  // Fungsi menghapus buku
  const deleteBook = (id) => {
    setBooks((prevBooks) => prevBooks.filter((book) => book.id !== id));
  };

  // Filter dan pencarian data buku menggunakan useMemo
  const filteredBooks = useMemo(() => {
    return books.filter((book) => {
      // Filter status
      const matchesStatus =
        filterStatus === 'semua' || book.status === filterStatus;

      // Filter query pencarian (judul atau penulis, case-insensitive)
      const query = searchQuery.trim().toLowerCase();
      const matchesQuery =
        query === '' ||
        book.title.toLowerCase().includes(query) ||
        book.author.toLowerCase().includes(query);

      return matchesStatus && matchesQuery;
    });
  }, [books, filterStatus, searchQuery]);

  // Buka modal untuk menambah buku baru
  const openAddModal = () => {
    setEditingBook(null);
    setIsFormOpen(true);
  };

  // Buka modal untuk mengedit buku tertentu
  const openEditModal = (book) => {
    setEditingBook(book);
    setIsFormOpen(true);
  };

  // Tutup modal form
  const closeFormModal = () => {
    setEditingBook(null);
    setIsFormOpen(false);
  };

  const value = {
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
  };

  return <BookContext.Provider value={value}>{children}</BookContext.Provider>;
}

BookProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

/**
 * Hook bantuan untuk menggunakan BookContext secara aman
 */
export function useBooks() {
  const context = useContext(BookContext);
  if (!context) {
    throw new Error('useBooks harus digunakan di dalam <BookProvider>');
  }
  return context;
}

export default BookContext;

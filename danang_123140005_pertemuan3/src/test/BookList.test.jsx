import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BookList } from '../components/BookList/BookList';

describe('Komponen BookList', () => {
  const sampleBooks = [
    {
      id: 'book-1',
      title: 'Laskar Pelangi',
      author: 'Andrea Hirata',
      status: 'milik',
      createdAt: '2026-01-01T00:00:00.000Z',
    },
    {
      id: 'book-2',
      title: 'Atomic Habits',
      author: 'James Clear',
      status: 'beli',
      createdAt: '2026-02-01T00:00:00.000Z',
    },
  ];

  it('menampilkan empty state jika daftar buku kosong', () => {
    render(
      <BookList
        books={[]}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
      />
    );

    expect(screen.getByText('Belum Ada Buku Ditemukan')).toBeInTheDocument();
  });

  it('merender kartu buku dengan judul, penulis, dan badge status yang tepat', () => {
    render(
      <BookList
        books={sampleBooks}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
      />
    );

    expect(screen.getByText('Laskar Pelangi')).toBeInTheDocument();
    expect(screen.getByText('Andrea Hirata')).toBeInTheDocument();
    expect(screen.getByText('Dimiliki')).toBeInTheDocument();

    expect(screen.getByText('Atomic Habits')).toBeInTheDocument();
    expect(screen.getByText('James Clear')).toBeInTheDocument();
    expect(screen.getByText('Ingin Dibeli')).toBeInTheDocument();
  });

  it('memanggil onEdit dan onDelete dengan data yang tepat saat tombol aksi diklik', async () => {
    const user = userEvent.setup();
    const handleEdit = vi.fn();
    const handleDelete = vi.fn();

    render(
      <BookList
        books={sampleBooks}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    );

    // Klik tombol edit pada buku pertama
    const editBtn = screen.getByLabelText('Edit Laskar Pelangi');
    await user.click(editBtn);
    expect(handleEdit).toHaveBeenCalledWith(sampleBooks[0]);

    // Klik tombol hapus pada buku pertama
    const deleteBtn = screen.getByLabelText('Hapus Laskar Pelangi');
    await user.click(deleteBtn);
    expect(handleDelete).toHaveBeenCalledWith('book-1', 'Laskar Pelangi');
  });
});

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BookForm } from '../components/BookForm/BookForm';

describe('Komponen BookForm (Validasi, Error Handling & Submit)', () => {
  it('tidak merender apa-apa jika isOpen bernilai false', () => {
    const { container } = render(
      <BookForm
        isOpen={false}
        onClose={vi.fn()}
        onSubmit={vi.fn()}
      />
    );
    expect(container.firstChild).toBeNull();
  });

  it('menampilkan pesan validasi error jika form disubmit dalam keadaan kosong', async () => {
    const user = userEvent.setup();
    const handleSubmit = vi.fn();

    render(
      <BookForm
        isOpen={true}
        onClose={vi.fn()}
        onSubmit={handleSubmit}
      />
    );

    // Klik tombol submit tanpa mengisi field
    const submitBtn = screen.getByRole('button', { name: /Tambah Buku/i });
    await user.click(submitBtn);

    // Validasi error harus muncul
    expect(screen.getByText('Judul buku wajib diisi')).toBeInTheDocument();
    expect(screen.getByText('Nama penulis wajib diisi')).toBeInTheDocument();
    expect(handleSubmit).not.toHaveBeenCalled();
  });

  it('memanggil onSubmit dengan data yang benar saat seluruh input valid', async () => {
    const user = userEvent.setup();
    const handleSubmit = vi.fn();
    const handleClose = vi.fn();

    render(
      <BookForm
        isOpen={true}
        onClose={handleClose}
        onSubmit={handleSubmit}
      />
    );

    const titleInput = screen.getByLabelText(/Judul Buku/i);
    const authorInput = screen.getByLabelText(/Nama Penulis/i);
    const statusRadio = screen.getByRole('radio', { name: /Sedang Dibaca/i });
    const submitBtn = screen.getByRole('button', { name: /Tambah Buku/i });

    await user.type(titleInput, 'Filosofi Teras');
    await user.type(authorInput, 'Henry Manampiring');
    await user.click(statusRadio);
    await user.click(submitBtn);

    expect(handleSubmit).toHaveBeenCalledWith({
      title: 'Filosofi Teras',
      author: 'Henry Manampiring',
      status: 'baca',
    });
    expect(handleClose).toHaveBeenCalled();
  });

  it('mengisi form otomatis dengan initialData saat mode edit', () => {
    const initialData = {
      id: 'book-99',
      title: 'Bumi Manusia',
      author: 'Pramoedya Ananta Toer',
      status: 'milik',
    };

    render(
      <BookForm
        isOpen={true}
        onClose={vi.fn()}
        onSubmit={vi.fn()}
        initialData={initialData}
      />
    );

    expect(screen.getByText('Edit Data Buku')).toBeInTheDocument();
    expect(screen.getByLabelText(/Judul Buku/i)).toHaveValue('Bumi Manusia');
    expect(screen.getByLabelText(/Nama Penulis/i)).toHaveValue('Pramoedya Ananta Toer');
    expect(screen.getByRole('radio', { name: /Dimiliki/i })).toBeChecked();
  });
});

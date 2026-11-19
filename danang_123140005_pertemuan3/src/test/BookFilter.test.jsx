import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BookFilter } from '../components/BookFilter/BookFilter';

describe('Komponen BookFilter', () => {
  const defaultCounts = {
    total: 10,
    milik: 5,
    baca: 3,
    beli: 2,
  };

  it('merender input pencarian dan tombol filter dengan counter yang sesuai', () => {
    render(
      <BookFilter
        searchQuery=""
        onSearchChange={vi.fn()}
        filterStatus="semua"
        onFilterChange={vi.fn()}
        counts={defaultCounts}
      />
    );

    expect(
      screen.getByPlaceholderText(/Cari buku berdasarkan judul/i)
    ).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Semua/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Dimiliki/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Sedang Dibaca/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Ingin Dibeli/i })).toBeInTheDocument();

    expect(screen.getByText('10')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  it('memanggil onSearchChange saat pengguna mengetik di input pencarian', async () => {
    const user = userEvent.setup();
    const handleSearch = vi.fn();

    render(
      <BookFilter
        searchQuery=""
        onSearchChange={handleSearch}
        filterStatus="semua"
        onFilterChange={vi.fn()}
        counts={defaultCounts}
      />
    );

    const input = screen.getByPlaceholderText(/Cari buku berdasarkan judul/i);
    await user.type(input, 'Filosofi');

    expect(handleSearch).toHaveBeenCalled();
  });

  it('memanggil onFilterChange dengan key yang sesuai saat tab status diklik', async () => {
    const user = userEvent.setup();
    const handleFilter = vi.fn();

    render(
      <BookFilter
        searchQuery=""
        onSearchChange={vi.fn()}
        filterStatus="semua"
        onFilterChange={handleFilter}
        counts={defaultCounts}
      />
    );

    const bacaTab = screen.getByRole('tab', { name: /Sedang Dibaca/i });
    await user.click(bacaTab);

    expect(handleFilter).toHaveBeenCalledWith('baca');
  });
});

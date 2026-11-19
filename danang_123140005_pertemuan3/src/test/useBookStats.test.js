import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useBookStats } from '../hooks/useBookStats';

describe('Custom Hook: useBookStats', () => {
  it('menghitung metrik dengan benar untuk daftar buku kosong', () => {
    const { result } = renderHook(() => useBookStats([]));

    expect(result.current.total).toBe(0);
    expect(result.current.milik).toBe(0);
    expect(result.current.baca).toBe(0);
    expect(result.current.beli).toBe(0);
    expect(result.current.milikPercent).toBe(0);
    expect(result.current.uniqueAuthors).toBe(0);
    expect(result.current.topAuthors).toEqual([]);
  });

  it('menghitung total, jumlah per status, dan persentase dengan tepat', () => {
    const dummyBooks = [
      { id: '1', title: 'Buku 1', author: 'Penulis A', status: 'milik' },
      { id: '2', title: 'Buku 2', author: 'Penulis A', status: 'milik' },
      { id: '3', title: 'Buku 3', author: 'Penulis B', status: 'baca' },
      { id: '4', title: 'Buku 4', author: 'Penulis C', status: 'beli' },
    ];

    const { result } = renderHook(() => useBookStats(dummyBooks));

    expect(result.current.total).toBe(4);
    expect(result.current.milik).toBe(2);
    expect(result.current.baca).toBe(1);
    expect(result.current.beli).toBe(1);
    expect(result.current.milikPercent).toBe(50);
    expect(result.current.bacaPercent).toBe(25);
    expect(result.current.beliPercent).toBe(25);
    expect(result.current.uniqueAuthors).toBe(3);
    expect(result.current.topAuthors[0]).toEqual({
      name: 'Penulis A',
      count: 2,
    });
  });
});

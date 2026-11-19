import { describe, it, expect, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useLocalStorage } from '../hooks/useLocalStorage';

describe('Custom Hook: useLocalStorage', () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it('mengembalikan initialValue jika localStorage masih kosong', () => {
    const { result } = renderHook(() =>
      useLocalStorage('test_key', 'default_value')
    );

    expect(result.current[0]).toBe('default_value');
  });

  it('mengambil nilai yang sudah ada di localStorage saat inisialisasi', () => {
    window.localStorage.setItem(
      'test_existing',
      JSON.stringify(['Buku A', 'Buku B'])
    );

    const { result } = renderHook(() =>
      useLocalStorage('test_existing', [])
    );

    expect(result.current[0]).toEqual(['Buku A', 'Buku B']);
  });

  it('memperbarui state dan menyinkronkan ke localStorage saat setter dipanggil', () => {
    const { result } = renderHook(() =>
      useLocalStorage('test_update', { count: 0 })
    );

    act(() => {
      result.current[1]({ count: 5 });
    });

    expect(result.current[0]).toEqual({ count: 5 });
    expect(JSON.parse(window.localStorage.getItem('test_update'))).toEqual({
      count: 5,
    });
  });
});

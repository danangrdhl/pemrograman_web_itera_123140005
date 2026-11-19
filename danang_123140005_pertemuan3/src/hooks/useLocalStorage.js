import { useState, useEffect } from 'react';

/**
 * Custom Hook untuk sinkronisasi state dengan localStorage
 * @param {string} key - Kunci penyimpanan localStorage
 * @param {any} initialValue - Nilai default jika key belum ada di localStorage
 * @returns {[any, Function]} - [storedValue, setValue]
 */
export function useLocalStorage(key, initialValue) {
  // Inisialisasi state dari localStorage dengan aman
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Gagal membaca key "${key}" dari localStorage:`, error);
      return initialValue;
    }
  });

  // Sinkronkan ke localStorage setiap kali storedValue atau key berubah
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error(`Gagal menyimpan key "${key}" ke localStorage:`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
}

export default useLocalStorage;

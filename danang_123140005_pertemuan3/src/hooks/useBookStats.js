import { useMemo } from 'react';

/**
 * Custom Hook untuk menghitung statistik koleksi buku
 * @param {Array} books - Daftar buku
 * @returns {Object} Statistik koleksi buku
 */
export function useBookStats(books = []) {
  return useMemo(() => {
    const total = books.length;
    const milik = books.filter((b) => b.status === 'milik').length;
    const baca = books.filter((b) => b.status === 'baca').length;
    const beli = books.filter((b) => b.status === 'beli').length;

    // Perhitungan persentase
    const milikPercent = total > 0 ? Math.round((milik / total) * 100) : 0;
    const bacaPercent = total > 0 ? Math.round((baca / total) * 100) : 0;
    const beliPercent = total > 0 ? Math.round((beli / total) * 100) : 0;

    // Hitung statistik penulis unik & buku per penulis
    const authorMap = {};
    books.forEach((b) => {
      const author = b.author?.trim();
      if (author) {
        authorMap[author] = (authorMap[author] || 0) + 1;
      }
    });

    const uniqueAuthors = Object.keys(authorMap).length;
    const topAuthors = Object.entries(authorMap)
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    return {
      total,
      milik,
      baca,
      beli,
      milikPercent,
      bacaPercent,
      beliPercent,
      uniqueAuthors,
      topAuthors,
    };
  }, [books]);
}

export default useBookStats;

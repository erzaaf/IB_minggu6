# Minggu 5 — Beyond Classical Search (IB 2026)

Sumber: `Minggu ke-6_Beyond Classical Search.pdf` + slide Latihan (55) dan Tugas Kelompok Kasus 02 (57-59).

## 1. Spesifikasi

### A. Latihan di Kelas (kertas, 1 iterasi)
- Puzzle grid 3x3, isi 1-9 berbeda, jumlah tiap baris & kolom sama (=15).
- Wajib: Hill Climbing, 4 tetangga.
- Opsi 1: Simulated Annealing.
- Opsi 2: Genetic Algorithm, populasi 4 individu.
- Tulis di kertas, kumpul akhir kuliah. Kelompok maks 3.

### B. Tugas Kelompok — Berbasis Kasus 02
1. Pilih 1 puzzle: N-Queen / Sudoku / Kakuro → repo ini pilih **N-Queen (8-Queen)**.
2. Selesaikan dengan **DFS-Backtracking** (+ optimasi: MRV, LCV, Forward Checking, Arc Consistency).
3. Selesaikan puzzle yang sama dengan **1 Local Search**: Hill Climbing / Simulated Annealing / Genetic Algorithm.
4. Bandingkan: kualitas solusi (optimal?) dan kecepatan pencarian.
5. Kelompok maks 3. Program bahasa bebas. Kumpul PDF `TugasKelompok_Rx_nim1_nim2_nim3.pdf` berisi hasil luaran program + analisis Backtracking vs Local Search. Durasi 1 minggu.

## 2. Isi Repo

- `latihan.py` — simulasi 1 step magic 3x3: Hill Climbing 4 tetangga, SA, GA 4 individu. Fungsi objektif `cost = sum|baris-15|+sum|kolom-15|`, `fitness = 36-cost`.
- `tugas_nqueen.py` — solver 8-Queen: DFS-Backtracking+FC, Hill Climbing+Restart, SA, GA. Representasi `state = list 8 angka`, `h = 28-attacks`, optimal `h=28`.

## 3. Cara Jalan

```powershell
python latihan.py
python tugas_nqueen.py
```

## 4. Hasil Ringkas (seed 42)

- DFS: `[1,6,8,3,7,4,2,5]` h=28 optimal, ~0.55ms, 47 nodes.
- Hill Climbing+Restart: optimal h=28.
- SA: optimal h=28.
- GA (pop20/gen200): h=27 tidak optimal → contoh trade-off.
- Latihan S0 `[[1,2,3],[4,5,6],[7,8,9]]`: HC plateau `12<=12` stop, SA terima sideways `prob=1.0`, GA I4 terbaik 40%.

## 5. Analisis (untuk PDF)

- Kualitas: DFS lengkap & optimal, Local bisa terjebak local maxima/plateau tanpa restart/sideways/probabilitas.
- Kecepatan: N=8 DFS masih menang `O(b^m)` kecil; N besar Local menang memori kecil & path-irrelevant.

# Tugas Kelompok Berbasis Kasus 02 — Beyond Classical Search

## Kasus: 8-Queen

Puzzle 8-Queen: taruh **8 ratu** di papan 8x8 supaya tidak ada yang saling serang (baris, kolom, diagonal).

Dipilih dari 3 opsi (N-Queen / Sudoku / Kakuro) karena paling pas dengan modul: contoh Hill Climbing, SA, dan GA di modul semuanya pakai 8-Queen.

Selesaikan 8-Queen dengan:
1. **DFS-Backtracking** (+ optimasi: MRV, LCV, Forward Checking)
2. **Local Search** — salah satu / semua dari:
   - Hill Climbing (+ Restart)
   - Simulated Annealing
   - Genetic Algorithm

Gunakan representasi kolom-per-kolom untuk DFS, dan representasi complete-state untuk Local Search.

Diskusikan perbedaan **kualitas solusi (optimal?) dan kecepatan pencarian** antara DFS-Backtracking vs Local Search.

---

## 1. Definisi Puzzle

Representasi (ikut modul):

| Elemen | Isi |
|--------|-----|
| State | `list 8 angka`, index = kolom 0-7, value = baris 1-8. Contoh `<1e 2f ...>` di modul = `[5,6,...]` di kode |
| Variable | Kolom `C0..C7` |
| Domain | Baris `{1..8}` per kolom |
| Constraint | `Ci != Cj` dan `|Ci-Cj| != |i-j|` untuk semua `i != j` |
| Initial | Acak (Local Search) / kosong (DFS) |
| Goal | `attacks = 0`, alias `h = 28` |

Total pasang ratu: `7+6+5+4+3+2+1 = 28`.

Start: `acak, misal [random 1-8 x8]`
Goal: `0 serangan`

---

## 2. Nilai Fungsi Objektif h(n)

Ikut modul hal 26-28, profit-oriented (makin besar makin baik):

| State | attacks | h = 28 - attacks | Status |
|-------|---------|------------------|--------|
| optimal | 0 | 28 | goal |
| hampir | 1 | 27 | local optimum |
| awal acak | ~10-17 | ~11-18 | contoh modul `h=11` |

Dipakai untuk Hill Climbing, SA (`delta = h_baru - h_lama`), dan GA (fitness).

Contoh hitung (modul): total 28, 1 pasang serang `1a-8h` → `h = 28-1 = 27`.

---

## 3. Yang Harus Dibuat

### Program sederhana (bahasa bebas, repo ini Python)

File: `tugas_nqueen.py`

Untuk tiap metode tampilkan:
- solusi `list 8 angka`
- jumlah `attacks` dan `h`
- waktu pencarian
- nodes / steps / iterasi / generasi

Khusus DFS-Backtracking:
- taruh ratu kolom-per-kolom
- pakai Forward Checking (hapus baris/diagonal yang diserang dari domain depan)
- ordering LCV/MRV untuk urutan baris
- tampilkan `nodes` yang diekspansi

Khusus Local Search:
- Hill Climbing: generate 56 tetangga (geser 1 ratu dalam 1 kolom), ambil `h` terbesar, restart jika stuck
- SA: ambil 1 tetangga acak, terima jika lebih baik atau `random < exp(delta/T)`, turunkan `T *= 0.95`
- GA: populasi (contoh 20), seleksi roulette dari fitness, crossover 1 titik, mutasi acak

Jalan:
```powershell
python tugas_nqueen.py
```

### Analisis perbandingan

- beda cara cari solusi DFS (incomplete → complete) vs Local (complete → complete, path-irrelevant)
- beda kualitas: DFS lengkap & optimal vs Local bisa stuck local maxima/plateau/shoulder
- beda kecepatan: `O(b^m)` DFS vs iterasi murah Local, plus memori
- pengaruh restart / temperatur / ukuran populasi pada Local Search

---

Mata kuliah: **Inteligensi Buatan — 2026**

# Tugas Kelompok Berbasis Kasus 02 — Beyond Classical Search

## Kasus: 8-Queen

Puzzle 8-Queen: taruh **8 ratu** di papan 8x8 supaya tidak ada yang saling serang (baris, kolom, diagonal).

Dipilih dari 3 opsi (N-Queen / Sudoku / Kakuro) karena ruang statusnya jelas terdefinisi, constraint-nya biner dan mudah diverifikasi, serta kedua pendekatan (konstruktif dan perbaikan iteratif) dapat diterapkan langsung untuk perbandingan yang adil.

Selesaikan 8-Queen dengan:
1. **DFS-Backtracking** (+ optimasi: MRV, LCV, Forward Checking)
2. **Local Search: Hill Climbing** (+ Restart)

Gunakan representasi kolom-per-kolom untuk DFS, dan representasi complete-state untuk Hill Climbing.

Diskusikan perbedaan **kualitas solusi (optimal?) dan kecepatan pencarian** antara DFS-Backtracking vs Local Search.

---

## 1. Definisi Puzzle

Representasi yang dipakai:

| Elemen | Isi |
|--------|-----|
| State | `list 8 angka`, index = kolom 0-7, value = baris 1-8. Contoh `<1e 2f ...>` = `[5,6,...]` di kode |
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

Bersifat profit-oriented (makin besar makin baik):

| State | attacks | h = 28 - attacks | Status |
|-------|---------|------------------|--------|
| optimal | 0 | 28 | goal |
| hampir | 1 | 27 | local optimum |
| awal acak | ~10-17 | ~11-18 | contoh `h=11` |

Dipakai untuk Hill Climbing (`h` terbesar menang, sideways/plateau = stop).

Contoh hitung: total 28, 1 pasang serang `1a-8h` → `h = 28-1 = 27`.

---

## 3. Yang Harus Dibuat

### Program sederhana


Untuk tiap metode tampilkan:
- solusi `list 8 angka`
- jumlah `attacks` dan `h`
- waktu pencarian
- nodes / steps

Khusus DFS-Backtracking:
- taruh ratu kolom-per-kolom
- pakai Forward Checking (hapus baris/diagonal yang diserang dari domain depan)
- ordering LCV/MRV untuk urutan baris
- tampilkan `nodes` yang diekspansi

Khusus Hill Climbing:
- generate 56 tetangga (geser 1 ratu dalam 1 kolom), ambil `h` terbesar
- restart dari state acak baru jika stuck di local maxima/plateau
- tampilkan `steps` sampai goal / restart habis


### Analisis perbandingan

- beda cara cari solusi DFS (incomplete → complete) vs Hill Climbing (complete → complete, path-irrelevant)
- beda kualitas: DFS lengkap & optimal vs Hill Climbing bisa stuck local maxima/plateau/shoulder
- beda kecepatan: `O(b^m)` DFS vs iterasi murah Hill Climbing, plus memori
- pengaruh jumlah restart pada Hill Climbing

---

Mata kuliah: **Inteligensi Buatan — 2026**
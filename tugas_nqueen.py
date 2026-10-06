"""8-Queen: DFS-Backtracking (MRV+LCV+FC+Branch&Bound) vs Hill Climbing (+Sideways+Restart)."""
import random
import statistics
import time

N = 8
TOTAL_PAIR = N * (N - 1) // 2  # 28
NEIGHBORS = N * (N - 1)  # 56 tetangga: geser 1 ratu dalam 1 kolom

# State awal dari soal (slide 57), koordinat (baris, kolom) 0-index:
#   (6,0) (5,1) (3,2) (3,3) (1,4) (3,5) (7,6) (3,7)
# Representasi kode: index = kolom 0-7, value = baris 1-8 (= baris slide + 1)
INITIAL_STATE = [7, 6, 4, 4, 2, 4, 8, 4]


def attacks(state):
    c = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                c += 1
    return c


def h(state):
    return TOTAL_PAIR - attacks(state)


def is_solution(state):
    return attacks(state) == 0


def moved(state, initial=INITIAL_STATE):
    """Jumlah ratu yang posisinya berbeda dari state awal (ukuran kualitas solusi)."""
    return sum(a != b for a, b in zip(state, initial))


def print_board(state):
    """Cetak papan dengan label (baris, kolom) 0-index seperti slide."""
    print("     " + " ".join(str(c) for c in range(N)))
    for r in range(N):
        print(f"  {r}  " + " ".join("Q" if state[c] == r + 1 else "." for c in range(N)))


# ---------- DFS BACKTRACKING + MRV + LCV + Forward Checking + Branch & Bound ----------
# Tujuan: solusi valid (attacks = 0) dengan jumlah ratu dipindah dari INITIAL_STATE paling sedikit.
# Degree heuristic tidak dipakai: setiap kolom berkonstrain dengan 7 kolom lain, jadi degree-nya selalu seri.
def dfs_backtracking(initial=INITIAL_STATE):
    stats = {"nodes": 0, "nodes_first": None}
    best = {"solution": None, "moved": N + 1}
    domains = [set(range(1, N + 1)) for _ in range(N)]
    t0 = time.perf_counter()
    _dfs([0] * N, domains, 0, initial, best, stats)
    return {
        "solution": best["solution"],
        "moved": best["moved"],
        "nodes_first": stats["nodes_first"],  # node sampai solusi pertama ditemukan
        "nodes": stats["nodes"],  # node sampai solusi optimal terbukti
        "time": time.perf_counter() - t0,
    }


def _dfs(sol, domains, moved_so_far, initial, best, stats):
    unassigned = [c for c in range(N) if sol[c] == 0]

    # Branch & Bound: kolom kosong yang baris awalnya sudah hilang dari domain pasti ikut dipindah
    lower_bound = moved_so_far + sum(initial[c] not in domains[c] for c in unassigned)
    if lower_bound >= best["moved"]:
        return

    if not unassigned:
        best["solution"] = list(sol)
        best["moved"] = moved_so_far
        if stats["nodes_first"] is None:
            stats["nodes_first"] = stats["nodes"]
        return

    col = min(unassigned, key=lambda c: (len(domains[c]), c))  # MRV

    def eliminated(r):  # banyak nilai di domain kolom lain yang hilang jika col = r
        cnt = 0
        for c2 in unassigned:
            if c2 != col:
                d = abs(c2 - col)
                cnt += len(domains[c2] & {r, r + d, r - d})
        return cnt

    # LCV, dengan baris dari state awal dicoba lebih dulu agar bound yang bagus cepat ditemukan
    candidates = sorted(domains[col], key=lambda r: (r != initial[col], eliminated(r)))
    for r in candidates:
        stats["nodes"] += 1
        new_domains = [set(d) for d in domains]
        new_domains[col] = {r}
        ok = True
        for c2 in unassigned:  # Forward Checking: hapus baris & diagonal yang diserang
            if c2 != col:
                d = abs(c2 - col)
                new_domains[c2] -= {r, r + d, r - d}
                if not new_domains[c2]:
                    ok = False
                    break
        if not ok:
            continue
        sol[col] = r
        _dfs(sol, new_domains, moved_so_far + (r != initial[col]), initial, best, stats)
        sol[col] = 0


# ---------- HILL CLIMBING + Sideways Move + Random Restart ----------
def random_state():
    return [random.randint(1, N) for _ in range(N)]


def best_neighbor(state):
    """Evaluasi 56 tetangga, ambil h terbesar (seri dipilih acak)."""
    best_h = -1
    best = []
    for col in range(N):
        for r in range(1, N + 1):
            if r == state[col]:
                continue
            nb = state[:]
            nb[col] = r
            hv = h(nb)
            if hv > best_h:
                best_h, best = hv, [nb]
            elif hv == best_h:
                best.append(nb)
    return random.choice(best), best_h


def hill_climbing(initial=INITIAL_STATE, max_restart=50, max_sideways=0):
    """Percobaan ke-0 dimulai dari `initial`, restart berikutnya dari state acak."""
    t0 = time.perf_counter()
    steps = evaluated = 0
    best_overall, best_h = None, -1
    for restart in range(max_restart + 1):
        cur = list(initial) if restart == 0 else random_state()
        cur_h = h(cur)
        sideways = 0
        while True:
            if cur_h > best_h:
                best_overall, best_h = cur[:], cur_h
            if cur_h == TOTAL_PAIR:
                break
            nb, nb_h = best_neighbor(cur)
            evaluated += NEIGHBORS
            if nb_h > cur_h:  # naik
                sideways = 0
            elif nb_h == cur_h and sideways < max_sideways:  # plateau: gerak menyamping
                sideways += 1
            else:  # local optimum / batas sideways habis
                break
            cur, cur_h = nb, nb_h
            steps += 1
        if cur_h == TOTAL_PAIR:
            break
    return {
        "solution": best_overall,
        "success": best_h == TOTAL_PAIR,
        "steps": steps,
        "restarts": restart,
        "evaluated": evaluated,
        "time": time.perf_counter() - t0,
        "moved": moved(best_overall, initial),
    }


# ---------- EKSPERIMEN PERBANDINGAN ----------
HC_VARIANTS = [
    ("HC murni", 0, 0),
    ("HC + restart", 50, 0),
    ("HC + sideways + restart", 50, 100),
]


def hc_success_rate(trials=1000):
    """Peluang sukses 1x HC murni dari state acak (pembanding p~0.14 di modul)."""
    return sum(hill_climbing(random_state(), max_restart=0)["success"] for _ in range(trials)) / trials


def run_experiment(trials=100):
    mean = statistics.mean
    header = f"{'Metode':<26}{'Sukses':>9}{'Steps':>8}{'Restart':>9}{'Dievaluasi':>12}{'Waktu(ms)':>11}{'Moved':>11}"
    print(header)
    print("-" * len(header))

    runs = [dfs_backtracking() for _ in range(trials)]  # deterministik, diulang hanya untuk rata-rata waktu
    d = runs[0]
    moved_col = f"{d['moved']:.2f}/{d['moved']}"
    print(f"{'DFS (MRV+LCV+FC+B&B)':<26}{f'{trials}/{trials}':>9}{'-':>8}{'-':>9}{d['nodes']:>12}"
          f"{mean(r['time'] for r in runs) * 1000:>11.3f}{moved_col:>11}")

    for name, max_restart, max_sideways in HC_VARIANTS:
        runs = [hill_climbing(max_restart=max_restart, max_sideways=max_sideways) for _ in range(trials)]
        ok = [r for r in runs if r["success"]]
        moved_col = f"{mean(r['moved'] for r in ok):.2f}/{min(r['moved'] for r in ok)}" if ok else "-"
        print(f"{name:<26}{f'{len(ok)}/{trials}':>9}{mean(r['steps'] for r in runs):>8.1f}"
              f"{mean(r['restarts'] for r in runs):>9.1f}{mean(r['evaluated'] for r in runs):>12.1f}"
              f"{mean(r['time'] for r in runs) * 1000:>11.3f}{moved_col:>11}")

    print(f"\nPeluang sukses 1x HC murni dari state acak (1000 percobaan): {hc_success_rate():.3f}")
    print("Moved = ratu dipindah dari state awal (rata-rata/minimum, hanya run yang sukses).")


if __name__ == "__main__":
    random.seed(42)
    print(f"=== 8-QUEEN: state awal dari soal (h_max={TOTAL_PAIR}, 0 serangan = goal) ===")
    print_board(INITIAL_STATE)
    print(f"state={INITIAL_STATE} attacks={attacks(INITIAL_STATE)} h={h(INITIAL_STATE)}\n")

    d = dfs_backtracking()
    print("[DFS-Backtracking: MRV + LCV + Forward Checking + Branch & Bound]")
    print_board(d["solution"])
    print(f"solusi={d['solution']} attacks={attacks(d['solution'])} h={h(d['solution'])} moved={d['moved']} "
          f"nodes_first={d['nodes_first']} nodes={d['nodes']} waktu={d['time'] * 1000:.2f}ms\n")

    for name, max_restart, max_sideways in (HC_VARIANTS[0], HC_VARIANTS[2]):
        r = hill_climbing(max_restart=max_restart, max_sideways=max_sideways)
        print(f"[{name}]")
        print_board(r["solution"])
        print(f"solusi={r['solution']} attacks={attacks(r['solution'])} h={h(r['solution'])} moved={r['moved']} "
              f"steps={r['steps']} restart={r['restarts']} dievaluasi={r['evaluated']} "
              f"waktu={r['time'] * 1000:.2f}ms sukses={r['success']}\n")

    print("=== EKSPERIMEN: 100 percobaan per metode, semua dari state awal soal ===")
    run_experiment()

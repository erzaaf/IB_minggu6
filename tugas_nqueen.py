"""8-Queen: DFS-Backtracking vs Hill Climbing."""
import random
import time

N = 8
TOTAL_PAIR = N * (N - 1) // 2  # 28


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


# ---------- DFS BACKTRACKING + Forward Checking + LCV ----------
dfs_nodes = 0


def dfs_backtracking():
    global dfs_nodes
    dfs_nodes = 0
    domains = [set(range(1, N + 1)) for _ in range(N)]
    sol = [0] * N
    t0 = time.perf_counter()
    res = _dfs(0, sol, domains)
    return res, (time.perf_counter() - t0), dfs_nodes


def _dfs(col, sol, domains):
    global dfs_nodes
    if col == N:
        return list(sol) if attacks(sol) == 0 else None

    def conflict_count(r):
        cnt = 0
        for c2 in range(col + 1, N):
            for r2 in domains[c2]:
                if r == r2 or abs(r - r2) == abs(col - c2):
                    cnt += 1
        return cnt

    candidates = sorted(domains[col], key=conflict_count)  # LCV
    for r in candidates:
        dfs_nodes += 1
        ok = True
        for pc in range(col):
            if sol[pc] == r or abs(sol[pc] - r) == abs(pc - col):
                ok = False
                break
        if not ok:
            continue
        sol[col] = r
        new_domains = [set(d) for d in domains]
        for c2 in range(col + 1, N):
            d = abs(c2 - col)
            new_domains[c2].discard(r)
            new_domains[c2].discard(r + d)
            new_domains[c2].discard(r - d)
            if not new_domains[c2]:
                ok = False
                break
        if not ok:
            continue
        res = _dfs(col + 1, sol, new_domains)
        if res:
            return res
    return None


# ---------- HILL CLIMBING ----------
def random_state():
    return [random.randint(1, N) for _ in range(N)]


def best_neighbor(state):
    cur_h = h(state)
    best = None
    best_h = cur_h
    for col in range(N):  # 56 tetangga: geser 1 ratu dalam 1 kolom
        for r in range(1, N + 1):
            if r == state[col]:
                continue
            nb = state[:]
            nb[col] = r
            hv = h(nb)
            if hv > best_h:
                best_h = hv
                best = nb
    return best, best_h


def hill_climbing(max_restart=20, max_steps=200):
    t0 = time.perf_counter()
    total_steps = 0
    best_overall = None
    best_h = -1
    for _ in range(max_restart):
        cur = random_state()
        for _ in range(max_steps):
            total_steps += 1
            nb, _ = best_neighbor(cur)
            if nb is None:  # local optimum / plateau
                break
            cur = nb
            if h(cur) > best_h:
                best_h = h(cur)
                best_overall = cur[:]
            if is_solution(cur):
                return cur, time.perf_counter() - t0, total_steps, True
    return best_overall, time.perf_counter() - t0, total_steps, is_solution(best_overall)


if __name__ == "__main__":
    random.seed(42)
    print(f"=== 8-QUEEN: h_max={TOTAL_PAIR} (0 serangan = optimal) ===")
    sol, t, nodes = dfs_backtracking()
    print(f"[DFS-Backtracking+FC] solusi={sol} attacks={attacks(sol)} h={h(sol)} waktu={t*1000:.2f}ms nodes={nodes} optimal={is_solution(sol)}")
    sol2, t2, steps2, ok2 = hill_climbing()
    print(f"[HillClimbing+Restart] solusi={sol2} attacks={attacks(sol2)} h={h(sol2)} waktu={t2*1000:.2f}ms steps={steps2} optimal={ok2}")

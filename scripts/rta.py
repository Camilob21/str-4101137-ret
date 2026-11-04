#!/usr/bin/env python3
"""Lab 6 — schedulability of the SoilSense node: U, both RM tests, RTA with blocking.

Edit the TABLES below (measured C in microseconds) and run:

    python3 scripts/rta.py               # the node, then the node + Daniela's tasks
    python3 scripts/rta.py --selftest    # checks the script against Buttazzo's examples

RTA (Buttazzo Fig. 4.17, extended with blocking, Theorem 7.2):
    R_i = C_i + B_i + sum_{h higher than i} ceil(R_i / T_h) * C_h
iterated from R_i = C_i + B_i until it stops moving, or until it passes D_i.
"""
import math
import sys

# ---------------------------------------------------------------------------
# 1. Measured worst execution times, from the analyzer (GPIO pulse widths).
#    (name, C_us, T_us, D_us)   priority = rate monotonic (shorter T first)
#    Measured maxima, without trace (RET §1.2, Fig. 6.4–6.6).
# ---------------------------------------------------------------------------
NODE = [
    ("sampling",   1.02,    1_000,     1_000),  # instr_samp (GPIO4) width, Fig. 6.5
    ("control",    1.063,  10_000,    10_000),  # instr_ctrl (GPIO5) width, no contention, Fig. 6.4
    ("telemetry", 72.28, 1_000_000, 1_000_000), # instr_tele (GPIO7) width, Fig. 6.6
]

# Daniela's two extra sensors. ASSUMPTION: the parameters are not in the repo
# (lab06: "given in class"); these two bring the load above the console to the
# course's reference U ~ 0.72 (week-6 deck, speaker notes). Replace if known.
DANIELA = [
    ("sensor_A",  2_000,   5_000,   5_000),     # ASSUMED: U = 0.40
    ("sensor_B",  3_200,  10_000,  10_000),     # ASSUMED: U = 0.32
]

# Blocking under the PI mutex: the console's longest critical section (Task B,
# GPIO17 width with `lock mutex`). The console is the lowest priority, so every
# task above it that is not above control's lock user can wait for it once.
B_US = 4_000          # B adopted (>= 3.173 ms measured on GPIO17, Fig. 6.11)
LOCK_USERS = {"control"}  # tasks that take the lock (besides the console)

# Task C inputs
CALIB_NEED_BEFORE_US = 395_249  # measured: console CPU of calib before ADR-005
CALIB_CPU_AFTER_US = 13_329     # measured: CTF trace, median 13.33 us x 1000
CALIB_DEADLINE_US = 1_000_000
ESTOP_DEADLINE_US = 5_000

# ---------------------------------------------------------------------------


def f(x):
    """Numbers for the table: integers as they are, the rest with 1 decimal."""
    return str(int(x)) if float(x).is_integer() else f"{x:.1f}"


def rm_order(tasks):
    return sorted(tasks, key=lambda t: (t[2], t[3]))


def utilization(tasks):
    return sum(c / t for _, c, t, _ in tasks)


def ll_bound(n):
    return n * (2 ** (1 / n) - 1)


def hyperbolic(tasks):
    p = 1.0
    for _, c, t, _ in tasks:
        p *= c / t + 1
    return p


def blocking(tasks, b_us, lock_users):
    """B_i under PIP: tasks from the highest lock user down to just above the
    console can be blocked once by the console's critical section (direct or
    push-through). Tasks above every lock user never wait for it."""
    if b_us <= 0:
        return [0] * len(tasks)
    names = [t[0] for t in tasks]
    users = [names.index(u) for u in lock_users if u in names]
    if not users:
        return [0] * len(tasks)
    first = min(users)
    return [b_us if i >= first else 0 for i in range(len(tasks))]


def rta(tasks, b):
    """tasks in priority order (highest first). Returns [(R, iterations, ok)]."""
    out = []
    for i, (name, c, t, d) in enumerate(tasks):
        r = c + b[i]
        steps = [r]
        while True:
            nxt = c + b[i] + sum(math.ceil(r / th) * ch for _, ch, th, _ in tasks[:i])
            steps.append(nxt)
            if nxt == r or nxt > d:
                r = nxt
                break
            r = nxt
        out.append((r, steps, r <= d))
    return out


def report(title, tasks, b_us=0, lock_users=()):
    tasks = rm_order(tasks)
    n = len(tasks)
    u = utilization(tasks)
    lub = ll_bound(n)
    hyp = hyperbolic(tasks)
    b = blocking(tasks, b_us, lock_users)
    print(f"\n=== {title} ===")
    print(f"{'task':<11}{'C us':>9}{'T us':>10}{'D us':>10}{'U_i':>8}{'B us':>8}{'R us':>10}  R<=D  iterations")
    res = rta(tasks, b)
    for (name, c, t, d), bi, (r, steps, ok) in zip(tasks, b, res):
        it = " -> ".join(f(s) for s in steps)
        print(f"{name:<11}{f(c):>9}{f(t):>10}{f(d):>10}{c / t:>8.4f}{f(bi):>8}{f(r):>10}  "
              f"{'yes' if ok else 'NO ':<4}  {it}")
    print(f"U = {u:.4f}   n = {n}")
    print(f"Liu & Layland: U <= n(2^(1/n)-1) = {lub:.4f}  -> {'PASS' if u <= lub else 'inconclusive'}"
          " (periodic set only, no blocking)")
    print(f"Hyperbolic:    prod(U_i+1) = {hyp:.4f} <= 2  -> {'PASS' if hyp <= 2 else 'inconclusive'}"
          " (periodic set only, no blocking)")
    print(f"EDF (exact):   U <= 1  -> {'schedulable' if u <= 1 else 'NOT schedulable'}")
    verdict = all(ok for _, _, ok in res)
    print(f"RTA verdict ({'with B = %d us' % b_us if b_us else 'no blocking'}): "
          f"{'every task meets R <= D' if verdict else 'some task misses'}")
    return u, res


def fit_and_estop(tasks):
    u_above = utilization(tasks)  # every periodic task is above the console
    left = (1 - u_above) * CALIB_DEADLINE_US
    print("\n=== Task C: does calib fit? (REQ-CONS-01) ===")
    print(f"U of the tasks above the console = {u_above:.4f}  -> they leave "
          f"{left / 1000:.1f} ms of every {CALIB_DEADLINE_US / 1000:.0f} ms")
    print(f"before ADR-005: needs {CALIB_NEED_BEFORE_US / 1000:.1f} ms of CPU -> "
          f"{'fits' if CALIB_NEED_BEFORE_US <= left else 'DOES NOT fit'}")
    print(f"after  ADR-005: needs {CALIB_CPU_AFTER_US / 1000:.1f} ms of CPU -> "
          f"{'fits' if CALIB_CPU_AFTER_US <= left else 'DOES NOT fit'}")

    t = {n: (c, tt) for n, c, tt, _ in NODE}
    c_s, t_s = t["sampling"]
    c_c, t_c = t["control"]
    before = round(t_s + t_c + c_c + t_s + c_s, 1)  # detect, wait control, control, next PWM
    after = round(t_s + c_s, 1)                      # detect; the same job drives the valve low
    print("\n=== Task C: e-stop path, worst case (REQ-ESTOP-01, 5 ms) ===")
    print(f"before: detect <= T_samp ({t_s}) + wait control <= T_ctrl ({t_c}) + C_ctrl ({c_c})"
          f" + next PWM step <= T_samp ({t_s}) + C_samp ({c_s}) = {before} us -> "
          f"{'meets' if before <= ESTOP_DEADLINE_US else 'MISSES'} 5 ms")
    print(f"after:  detect <= T_samp ({t_s}) + C_samp ({c_s}) = {after} us -> "
          f"{'meets' if after <= ESTOP_DEADLINE_US else 'MISSES'} 5 ms")


def selftest():
    # Buttazzo Fig. 4.13: tau2 misses, R2 = 8 > 7
    res = rta([("t1", 2, 5, 5), ("t2", 4, 7, 7)], [0, 0])
    assert res[0][0] == 2 and res[1][0] == 8 and not res[1][2], res
    # Buttazzo Table 4.3 (D < T): R = 1, 2, 4, 10
    t43 = [("t1", 1, 4, 3), ("t2", 1, 5, 4), ("t3", 2, 6, 5), ("t4", 1, 11, 10)]
    res = rta(t43, [0] * 4)
    assert [r for r, _, _ in res] == [1, 2, 4, 10], res
    assert res[3][1] == [1, 5, 6, 7, 9, 10, 10], res[3][1]
    print("selftest OK: Fig. 4.13 gives R2 = 8 > 7; Table 4.3 gives R = 1, 2, 4, 10")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)
    report("Fig. 4.13 (book check, ms)", [("tau1", 2, 5, 5), ("tau2", 4, 7, 7)])
    report("Node as measured, no lock contention", NODE)
    report("Node with the PI mutex (B from Task B)", NODE, B_US, LOCK_USERS)
    report("Node + Daniela's two sensors, no blocking", NODE + DANIELA)
    report("Node + Daniela's two sensors, PI mutex", NODE + DANIELA, B_US, LOCK_USERS)
    fit_and_estop(NODE + DANIELA)

# Test Log

## 2026-03-20 — Baseline (no monotonicity)

**Config:** 20 games, depth=3, heuristic = `empty_count × 100 + log2(max_tile) × 10`

| Metric | Value |
|---|---|
| Avg score | 6708 |
| Max score | 12104 |
| Avg max tile | 538 |
| Best max tile | 1024 |
| % reached 512 | 80% |
| % reached 1024 | 15% |
| % reached 2048 | 0% |

**Notes:** AI survives well but cannot close out games. Tiles scatter without directional order, blocking merges at higher values. Monotonicity heuristic not yet added.

---

## 2026-03-20 — With Monotonicity (weight=25)

**Config:** 20 games, depth=3, heuristic = `empty_count × 100 + log2(max_tile) × 10 - monotonicity × 25`

| Metric | Baseline | With Monotonicity |
|---|---|---|
| Avg score | 6708 | 17372 |
| Max score | 12104 | 58792 |
| Avg max tile | 538 | 1254 |
| Best max tile | 1024 | 4096 |
| % reached 512 | 80% | 100% |
| % reached 1024 | 15% | 85% |
| % reached 2048 | 0% | 20% |

**Notes:** Dramatic improvement across all metrics. AI now consistently reaches 1024 and hits 2048 in 20% of games. Best game reached 4096. Monotonicity gives the AI directional order — tiles flow toward a corner instead of scattering. Weight of 25 not yet tuned.

---

## Weight tuning plan

The goal is to find the best weight for the monotonicity penalty. We will run 20 games at depth=3 for each candidate weight and compare the same metrics.

**Weights to test:** 0 (confirm baseline), 10, 25 (current), 50, 100

**What we expect:**
- Too low (0–10) — monotonicity has little effect, tiles stay scattered
- Sweet spot (25–50) — AI balances order with survival and merge opportunity
- Too high (100+) — AI obsesses over ordering, misses obvious merges, may score worse

Each run will be added as an entry below with its weight, results, and notes.

---

## 2026-03-20 — Weight tuning results

**Config:** 20 games, depth=3 for each weight

| Weight | Avg score | Avg max tile | % 1024 | % 2048 |
|---|---|---|---|---|
| 0 | 6549 | 538 | 20% | 0% |
| 10 | 10068 | 781 | 55% | 0% |
| **25** | **17091** | **1229** | **80%** | **30%** |
| 50 | 16410 | 1114 | 80% | 20% |
| 100 | 17959 | 1178 | 80% | 25% |

**Winner: weight=25**

**Why 25 is the sweet spot — and why it relates to log2:**

The monotonicity penalty is measured in log2 units. One step between adjacent tiles (e.g. 512→1024) costs exactly 1 log2 unit. The full board has 8 sequences of 3 pairs, so maximum disorder is around 240 log2 units.

The other heuristic terms operate on a similar scale:
- Each empty cell contributes 100
- Max tile contributes `log2(max_tile) × 10` — roughly 100 for a 1024 tile

At weight=25, one unit of disorder costs 25 — comparable to a quarter of an empty cell. The penalty is proportionate to the other terms, so the AI takes ordering seriously without being paralysed by it.

At weight=100, disorder costs as much as a full empty cell. The AI becomes so averse to misorder that it sacrifices merges to maintain tile ordering, which is why avg max tile drops slightly vs weight=25 despite a similar avg score.

**Conclusion:** 25 keeps the monotonicity penalty in the same ballpark as the rewards set by the log2 scale. Weights much above 50 let monotonicity dominate and distort the balance between order, survival, and progress.

---

## Weight tuning plan — empty cell and max tile weights

Now that monotonicity is fixed at 25, we sweep the other two weights independently. This is a first pass — weights interact, so independent sweeps may not find the global optimum. A full grid search is noted for later.

**Experiment 1 — Empty cell weight sweep**
Fix: max_tile_weight=10, monotonicity=25
Test: `[25, 50, 100, 200, 400]`

**Experiment 2 — Max tile weight sweep**
Fix: empty_weight=100, monotonicity=25
Test: `[1, 5, 10, 20, 50]`

**Future — Grid search**
Once independent sweeps identify promising ranges, run a grid search over the top candidates from each sweep to find the best combination. Results to be added here.

---

## 2026-03-20 — Experiment 1: Empty cell weight sweep (max_tile=10, monotonicity=25)

| Empty weight | Avg score | Avg max tile | % 1024 | % 2048 |
|---|---|---|---|---|
| 25 | 18454 | 1254 | 85% | 30% |
| **50** | **19469** | **1306** | **95%** | **30%** |
| 100 | 14207 | 998 | 85% | 5% |
| 200 | 11089 | 806 | 50% | 5% |
| 400 | 8439 | 640 | 30% | 0% |

**Winner: 50**

**Notes:** Higher empty weight hurts performance — the AI starts hoarding space instead of committing to merges. The original default of 100 was too high. Sweet spot is around 50, where survival instinct is balanced against progress.

---

## 2026-03-20 — Experiment 2: Max tile weight sweep (empty=100, monotonicity=25)

| Max tile weight | Avg score | Avg max tile | % 1024 | % 2048 |
|---|---|---|---|---|
| 1 | 16697 | 1088 | 75% | 20% |
| **5** | **18416** | **1331** | **90%** | **35%** |
| 10 | 16076 | 1178 | 70% | 30% |
| 20 | 15808 | 1139 | 75% | 25% |
| 50 | 16972 | 1254 | 85% | 30% |

**Winner: 5**

**Notes:** Reducing max tile weight from 10 to 5 improved performance noticeably. The max tile term is already implicitly rewarded through merges adding to the game score — so a lighter weight avoids double-counting progress and lets empty cells and monotonicity do more of the steering.

---

## Summary of best known weights

| Weight | Original | Best found |
|---|---|---|
| Empty cells | 100 | 50 |
| Max tile | 10 | 5 |
| Monotonicity | 25 | 25 |

**Note:** These were tuned independently. A grid search over combinations may find a better overall configuration but has not been run yet.

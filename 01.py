from collections import deque

# ─── Назви вершин ───────────────────────────────────────────────
NODE_NAMES = {
    0:  "Джерело (супер-джерело)",
    1:  "Термінал 1",
    2:  "Термінал 2",
    3:  "Склад 1",
    4:  "Склад 2",
    5:  "Склад 3",
    6:  "Склад 4",
    7:  "Магазин 1",
    8:  "Магазин 2",
    9:  "Магазин 3",
    10: "Магазин 4",
    11: "Магазин 5",
    12: "Магазин 6",
    13: "Магазин 7",
    14: "Магазин 8",
    15: "Магазин 9",
    16: "Магазин 10",
    17: "Магазин 11",
    18: "Магазин 12",
    19: "Магазин 13",
    20: "Магазин 14",
    21: "Стік (супер-стік)",
}

N = 22          # загальна кількість вершин
SOURCE = 0      # супер-джерело
SINK   = 21     # супер-стік


def build_capacity_matrix() -> list[list[int]]:
    """Будує матрицю пропускних здатностей для логістичної мережі."""
    cap = [[0] * N for _ in range(N)]

    # Супер-джерело → термінали (сума вихідних ребер кожного терміналу)
    cap[0][1] = 60   # Термінал 1: 25+20+15
    cap[0][2] = 55   # Термінал 2: 15+30+10

    # ── Термінал 1 → склади ────────────────────────────────────
    cap[1][3] = 25   # T1 → Склад 1
    cap[1][4] = 20   # T1 → Склад 2
    cap[1][5] = 15   # T1 → Склад 3

    # ── Термінал 2 → склади ────────────────────────────────────
    cap[2][5] = 15   # T2 → Склад 3
    cap[2][6] = 30   # T2 → Склад 4
    cap[2][4] = 10   # T2 → Склад 2

    # ── Склад 1 → магазини 1–3 ────────────────────────────────
    cap[3][7]  = 15
    cap[3][8]  = 10
    cap[3][9]  = 20

    # ── Склад 2 → магазини 4–6 ────────────────────────────────
    cap[4][10] = 15
    cap[4][11] = 10
    cap[4][12] = 25

    # ── Склад 3 → магазини 7–9 ────────────────────────────────
    cap[5][13] = 20
    cap[5][14] = 15
    cap[5][15] = 10

    # ── Склад 4 → магазини 10–14 ─────────────────────────────
    cap[6][16] = 20
    cap[6][17] = 10
    cap[6][18] = 15
    cap[6][19] = 5
    cap[6][20] = 10

    # ── Магазини → супер-стік (необмежена ємність) ───────────
    for shop in range(7, 21):
        cap[shop][21] = 10_000

    return cap


# ─── BFS (пошук збільшуючого шляху у залишковій мережі) ───────
def bfs(graph: list[list[int]], source: int, sink: int,
        parent: list[int]) -> bool:
    """
    Обхід у ширину залишкової мережі.
    Повертає True, якщо знайдено шлях від source до sink.
    Заповнює масив parent для відновлення шляху.
    """
    visited = {source}
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for v in range(N):
            if v not in visited and graph[u][v] > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False


# ─── Алгоритм Едмондса–Карпа ──────────────────────────────────
def edmonds_karp(cap: list[list[int]], source: int, sink: int
                 ) -> tuple[int, list[list[int]], list[dict]]:
    """
    Алгоритм Едмондса–Карпа для знаходження максимального потоку.

    Параметри:
        cap    – матриця початкових пропускних здатностей
        source – індекс джерела
        sink   – індекс стоку

    Повертає:
        max_flow   – значення максимального потоку
        residual   – залишкова мережа після насичення
        iterations – список словників із деталями кожної ітерації
    """
    # Копія матриці — залишкова мережа
    residual = [row[:] for row in cap]
    max_flow = 0
    iterations = []

    while True:
        parent = [-1] * N
        if not bfs(residual, source, sink, parent):
            break  # збільшуючого шляху більше не існує

        # Знайти мінімальне залишкове ребро вздовж знайденого шляху
        path_flow = float('inf')
        path_edges: list[tuple[int, int]] = []
        v = sink
        while v != source:
            u = parent[v]
            path_edges.append((u, v))
            path_flow = min(path_flow, residual[u][v])
            v = parent[v]
        path_edges.reverse()

        # Оновити залишкові ємності (пряме ребро зменшується, зворотне зростає)
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow

        # Зберегти деталі ітерації
        path_names = [NODE_NAMES[u] for u, _ in path_edges] + [NODE_NAMES[path_edges[-1][1]]]
        iterations.append({
            "path":       " → ".join(path_names),
            "path_edges": path_edges,
            "flow":       path_flow,
            "total":      max_flow,
        })

    return max_flow, residual, iterations


# ─── Виведення результатів ─────────────────────────────────────
def print_results(cap, max_flow, residual, iterations):
    SEP = "─" * 70

    print(SEP)
    print(f"  АЛГОРИТМ ЕДМОНДСА–КАРПА · ЛОГІСТИЧНА МЕРЕЖА")
    print(SEP)
    print(f"\n  ✅ Максимальний потік: {max_flow} одиниць товару\n")

    print(SEP)
    print("  ПОКРОКОВА РОБОТА АЛГОРИТМУ")
    print(SEP)
    for i, it in enumerate(iterations, 1):
        print(f"\n  Ітерація {i:>2}:")
        print(f"    Шлях : {it['path']}")
        print(f"    Потік: +{it['flow']} од.  (всього = {it['total']})")

    print(f"\n{SEP}")
    print("  ПОТОКИ ЧЕРЕЗ ТЕРМІНАЛИ")
    print(SEP)
    terminals = [(1, "Термінал 1", [3, 4, 5]),
                 (2, "Термінал 2", [4, 5, 6])]
    for tid, tname, warehouses in terminals:
        outflow = sum(cap[tid][w] - residual[tid][w] for w in warehouses)
        capacity = sum(cap[tid][w] for w in warehouses)
        pct = outflow / capacity * 100 if capacity else 0
        print(f"  {tname}: {outflow}/{capacity} ({pct:.0f}%)")

    print(f"\n{SEP}")
    print("  ПОТОКИ ЧЕРЕЗ СКЛАДИ")
    print(SEP)
    warehouses = [
        (3, "Склад 1", [1],    list(range(7, 10))),
        (4, "Склад 2", [1, 2], list(range(10, 13))),
        (5, "Склад 3", [1, 2], list(range(13, 16))),
        (6, "Склад 4", [2],    list(range(16, 21))),
    ]
    for wid, wname, sources, shops in warehouses:
        inflow  = sum(cap[t][wid] - residual[t][wid] for t in sources)
        max_in  = sum(cap[t][wid] for t in sources)
        out_cap = sum(cap[wid][s] for s in shops)
        print(f"  {wname}: вхід {inflow}/{max_in}  |  макс. вихід {out_cap}")

    print(f"\n{SEP}")
    print("  ЗАВАНТАЖЕНІСТЬ РЕБЕР СКЛАДИ → МАГАЗИНИ")
    print(SEP)
    shop_names = {7:"М1",8:"М2",9:"М3",10:"М4",11:"М5",12:"М6",
                  13:"М7",14:"М8",15:"М9",16:"М10",17:"М11",
                  18:"М12",19:"М13",20:"М14"}
    for wid, wname, _, shops in warehouses:
        for s in shops:
            flow = cap[wid][s] - residual[wid][s]
            c    = cap[wid][s]
            pct  = flow / c * 100 if c else 0
            bar  = "█" * int(pct // 10) + "░" * (10 - int(pct // 10))
            status = wtype(pct)
            print(f"  {wname} → {shop_names[s]:>3}: {flow:>2}/{c:>2}  [{bar}] {pct:>5.1f}%  {status}")

    print(f"\n{SEP}")
    print("  АНАЛІЗ ТА ВИСНОВКИ")
    print(SEP)
    print("""
  1. Максимальний потік = 115 одиниць — оптимальний результат (теорема
     Форда–Фалкерсона: max-flow = min-cut).

  2. Обидва термінали використовуються на 100%. Вузькі місця — вхідні
     ребра до складів з Термінала 1 (T1→С1=25, T1→С3=15) та
     Термінала 2 (T2→С3=15, T2→С4=30).

  3. Склади мають значний резерв на виході (особливо Склад 4: лише 50%
     вихідної ємності використано). Для збільшення потоку потрібно
     нарощувати вхідну ємність складів, а не вихідну.

  4. 5 магазинів (М3, М9, М12, М13, М14) не отримують товар — через
     обмеження на рівні терміналів та складів, а не через відсутність
     вихідних ребер.

  5. Алгоритм виконав 11 BFS-ітерацій; складність O(V·E²) = O(22·400)
     — надзвичайно швидко для мереж такого розміру.
""")

def wtype(pct):
    status = "✅ насичене" if pct == 100 else ("⚠️ часткове" if pct > 0 else "⬜ пусте   ")
    return status


# ─── Точка входу ──────────────────────────────────────────────
if __name__ == "__main__":
    cap = build_capacity_matrix()
    max_flow, residual, iterations = edmonds_karp(cap, SOURCE, SINK)
    print_results(cap, max_flow, residual, iterations)

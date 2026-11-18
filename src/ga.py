"""Thuật toán di truyền chọn tổ hợp nhóm đặc trưng cho CRF.

Cá thể  : vector bit, bit g = 1 nghĩa là bật nhóm FEATURE_GROUPS[g]
Fitness : token accuracy k-fold trên (tập con của) train, trừ phạt `penalty` cho mỗi nhóm bật.
          KHÔNG dùng dev/test.
Vòng lặp: giữ `elite` cá thể tốt nhất, phần còn lại sinh bằng chọn lọc giải đấu (tournament),
          lai ghép đồng đều (uniform crossover) và đột biến lật bit.

Chạy:  python -m src.ga --lang vi
"""

# - [x] cá thể = vector bit, mỗi bit bật/tắt một nhóm trong FEATURE_GROUPS
# - [x] fitness = điểm k-fold trên train (KHÔNG dùng dev/test), có trừ phạt số nhóm
# - [x] chọn lọc, lai ghép, đột biến; ghi fitness theo thế hệ để vẽ hình
# - [x] so sánh kết quả GA với ablation thủ công (results/tables/ablation_*.md) và với L1

import argparse
import json
import random
import statistics
import sys
from pathlib import Path

from src.crf import CRFTagger
from src.features import ALL_GROUPS
from src.model_selection import cross_val_score, subsample


def decode(bits):
    return tuple(g for g, b in zip(ALL_GROUPS, bits) if b)


class FeatureGA:
    def __init__(self, sentences, k=2, penalty=0.002, pop_size=8, generations=6, elite=2,
                 p_mut=0.15, crf_params=None, seed=42):
        self.sentences, self.k, self.penalty = sentences, k, penalty
        self.pop_size, self.generations, self.elite, self.p_mut = pop_size, generations, elite, p_mut
        self.crf_params = crf_params or {}
        self.rng = random.Random(seed)
        self.seed = seed
        self.cache = {}

    def fitness(self, bits):
        bits = tuple(bits)
        if bits not in self.cache:
            if not any(bits):
                self.cache[bits] = (0.0, 0.0)
            else:
                params = {**self.crf_params, "groups": decode(bits)}
                acc = statistics.mean(cross_val_score(CRFTagger, params, self.sentences, self.k, self.seed))
                self.cache[bits] = (acc - self.penalty * sum(bits), acc)
        return self.cache[bits][0]

    def _tournament(self, pop, size=3):
        return max(self.rng.sample(pop, size), key=self.fitness)

    def _child(self, pop):
        a, b = self._tournament(pop), self._tournament(pop)
        child = [x if self.rng.random() < 0.5 else y for x, y in zip(a, b)]
        return tuple(1 - x if self.rng.random() < self.p_mut else x for x in child)

    def run(self, log=print):
        n = len(ALL_GROUPS)
        pop = [tuple([1] * n)] + [tuple(self.rng.randint(0, 1) for _ in range(n))
                                  for _ in range(self.pop_size - 1)]
        history = []
        for gen in range(self.generations):
            pop.sort(key=self.fitness, reverse=True)
            fits = [self.fitness(p) for p in pop]
            history.append({"gen": gen, "best": fits[0], "mean": statistics.mean(fits),
                            "best_groups": decode(pop[0]), "best_acc": self.cache[pop[0]][1]})
            log(f"thế hệ {gen}: best={fits[0]:.4f} mean={statistics.mean(fits):.4f} {decode(pop[0])}")
            pop = pop[:self.elite] + [self._child(pop) for _ in range(self.pop_size - self.elite)]
        best = max(self.cache, key=lambda b: self.cache[b][0])
        return decode(best), history


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    from src.data import load

    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="vi")
    parser.add_argument("--frac", type=float, default=0.3, help="tập con train để fitness rẻ hơn")
    parser.add_argument("--generations", type=int, default=6)
    parser.add_argument("--pop", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    config = json.loads((root / "configs" / "best_params.json").read_text(encoding="utf-8"))
    crf_params = {k: v for k, v in config.get(args.lang, {}).get("crf", {}).items() if not k.startswith("_")}
    train = subsample(load(args.lang, "train"), args.frac, args.seed)
    ga = FeatureGA(train, pop_size=args.pop, generations=args.generations,
                   crf_params={**crf_params, "max_iterations": 50}, seed=args.seed)
    best, history = ga.run()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([h["gen"] for h in history], [h["best"] for h in history], marker="o", label="tốt nhất")
    ax.plot([h["gen"] for h in history], [h["mean"] for h in history], marker="s", label="trung bình")
    ax.set_xlabel("thế hệ")
    ax.set_ylabel("fitness (acc k-fold - phạt)")
    ax.set_title(f"GA chọn nhóm đặc trưng CRF ({args.lang})")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(root / "results" / "figures" / f"ga_{args.lang}.png", dpi=150)

    lines = [f"# GA chọn nhóm đặc trưng CRF ({args.lang})", "",
             f"Tập con train frac={args.frac}, k={ga.k}, phạt {ga.penalty}/nhóm, seed={args.seed}", "",
             f"**Tốt nhất:** {', '.join(best)}", "",
             "| Thế hệ | Fitness tốt nhất | Acc của cá thể tốt nhất | TB quần thể | Nhóm |", "|---|---|---|---|---|"]
    lines += [f"| {h['gen']} | {h['best']:.4f} | {h['best_acc']:.4f} | {h['mean']:.4f} | "
              f"{', '.join(h['best_groups'])} |" for h in history]
    out = root / "results" / "tables" / f"ga_{args.lang}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Đã ghi", out.relative_to(root))


if __name__ == "__main__":
    main()

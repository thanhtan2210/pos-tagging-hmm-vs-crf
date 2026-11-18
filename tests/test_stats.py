from src.stats import mcnemar, paired_bootstrap

GOLD = [(["a", "b", "c"], ["X", "Y", "Z"]), (["d", "e"], ["X", "X"])] * 10


def recs(preds):
    return [(w, g, p) for (w, g), p in zip(GOLD, preds)]


def test_identical_models():
    a = recs([["X", "Y", "Y"], ["X", "X"]] * 10)
    diff, (lo, hi) = paired_bootstrap(a, a, n=200, seed=0)
    assert diff == 0 and lo <= 0 <= hi
    assert mcnemar(a, a) == (0, 0, 1.0)


def test_mcnemar_balanced_and_unbalanced():
    a = recs([["X", "Y", "Y"], ["Y", "X"]] * 10)  # sai ở câu 1 token 3, câu 2 token 1
    b = recs([["X", "Y", "Z"], ["Y", "Y"]] * 10)
    nb, nc, p = mcnemar(a, b)
    assert (nb, nc) == (10, 10) and p > 0.5  # b = c -> p lớn
    good = recs([["X", "Y", "Z"], ["X", "X"]] * 10)
    nb, nc, p = mcnemar(good, a)
    assert nb == 20 and nc == 0 and p < 0.001
    diff, (lo, hi) = paired_bootstrap(good, a, n=200, seed=0)
    assert diff > 0 and lo > 0

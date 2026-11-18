from src.baseline import MostFrequentTagger
from src.model_selection import grid_search, kfold_sentences, param_grid, subsample

SENTS = [([f"w{i}", "x"], ["A", "B"]) for i in range(23)]


def test_kfold_disjoint_and_complete():
    splits = kfold_sentences(SENTS, k=5, seed=1)
    vals = [s for _, val in splits for s in val]
    assert sorted(vals) == sorted(SENTS)  # mỗi câu đúng 1 lần ở val
    for train, val in splits:
        assert len(train) + len(val) == len(SENTS)
        assert not set(map(str, train)) & set(map(str, val))


def test_kfold_reproducible():
    assert kfold_sentences(SENTS, 4, seed=7) == kfold_sentences(SENTS, 4, seed=7)
    assert kfold_sentences(SENTS, 4, seed=7) != kfold_sentences(SENTS, 4, seed=8)


def test_subsample_size():
    assert len(subsample(SENTS, 0.5, seed=0)) == round(23 * 0.5)
    assert len(subsample(SENTS, 1.0)) == 23


def test_param_grid_and_grid_search():
    assert param_grid({"a": [1, 2], "b": [3]}) == [{"a": 1, "b": 3}, {"a": 2, "b": 3}]
    best, table = grid_search(MostFrequentTagger, {"oov": ["default", "signature"]}, SENTS, k=3)
    assert best["oov"] in ("default", "signature")
    assert len(table) == 2

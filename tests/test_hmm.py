import itertools

import numpy as np

from src.hmm import UNK, HMMTagger, viterbi

TOY = [
    (["tôi", "ăn", "cơm"], ["PRON", "VERB", "NOUN"]),
    (["tôi", "đọc", "sách"], ["PRON", "VERB", "NOUN"]),
    (["sách", "hay"], ["NOUN", "ADJ"]),
]


def brute_force(log_pi, log_A, log_emit):
    """Thử mọi chuỗi nhãn, chỉ dùng được với T và n rất nhỏ."""
    T, n = log_emit.shape
    best, best_score = None, -np.inf
    for path in itertools.product(range(T), repeat=n):
        score = log_pi[path[0]] + log_emit[path[0], 0]
        for k in range(1, n):
            score += log_A[path[k - 1], path[k]] + log_emit[path[k], k]
        if score > best_score:
            best, best_score = list(path), score
    return best


def random_log_dist(rng, *shape):
    p = rng.random(shape) + 1e-3
    return np.log(p / p.sum(axis=-1, keepdims=True))


def test_viterbi_matches_brute_force():
    rng = np.random.default_rng(0)
    for _ in range(50):
        T, n = int(rng.integers(2, 5)), int(rng.integers(1, 6))
        log_pi = random_log_dist(rng, T)
        log_A = random_log_dist(rng, T, T)
        log_emit = np.log(rng.random((T, n)) + 1e-3)
        assert list(viterbi(log_pi, log_A, log_emit)) == brute_force(log_pi, log_A, log_emit)


def test_fit_rows_are_distributions():
    m = HMMTagger(alpha=0.1).fit(TOY)
    assert np.isclose(np.exp(m.log_pi).sum(), 1)
    assert np.allclose(np.exp(m.log_A).sum(axis=1), 1)
    assert np.allclose(np.exp(m.log_B).sum(axis=1), 1)


def test_fit_counts_match_hand_computation():
    m = HMMTagger(alpha=1e-9).fit(TOY)  # alpha gần 0 -> gần như MLE thuần
    t, w = m.tag2id, m.word2id
    assert np.isclose(np.exp(m.log_pi[t["PRON"]]), 2 / 3)
    assert np.isclose(np.exp(m.log_A[t["PRON"], t["VERB"]]), 1.0)
    assert np.isclose(np.exp(m.log_A[t["NOUN"], t["ADJ"]]), 1.0)
    assert np.isclose(np.exp(m.log_B[t["NOUN"], w["sách"]]), 2 / 3)
    assert np.isclose(np.exp(m.log_B[t["VERB"], w["ăn"]]), 1 / 2)


def test_predict_on_toy():
    m = HMMTagger(alpha=0.1).fit(TOY)
    assert m.predict(["tôi", "đọc", "cơm"]) == ["PRON", "VERB", "NOUN"]
    assert len(m.predict(["từ_lạ", "hay"])) == 2  # từ lạ không làm lỗi
    assert UNK in m.word2id

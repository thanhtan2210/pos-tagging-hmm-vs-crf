from src.crf import CRFTagger
from src.features import ALL_GROUPS, word2features

TOY = [
    (["tôi", "ăn", "cơm"], ["PRON", "VERB", "NOUN"]),
    (["tôi", "đọc", "sách"], ["PRON", "VERB", "NOUN"]),
    (["sách", "hay"], ["NOUN", "ADJ"]),
] * 5


def test_crf_fit_predict_lengths():
    m = CRFTagger(c1=0.0, c2=0.01, max_iterations=50).fit(TOY)
    assert m.predict(["tôi", "đọc", "cơm"]) == ["PRON", "VERB", "NOUN"]
    assert len(m.predict(["từ lạ", "hay"])) == 2
    assert m.predict([]) == []


def test_dropping_group_removes_only_its_keys():
    words = ["Hà Nội", "có", "123", "người"]
    full = word2features(words, 1, ALL_GROUPS)
    for g in ALL_GROUPS:
        rest = word2features(words, 1, [x for x in ALL_GROUPS if x != g])
        assert not any(k.startswith(g + ":") for k in rest)
        assert {k: v for k, v in full.items() if not k.startswith(g + ":")} == rest

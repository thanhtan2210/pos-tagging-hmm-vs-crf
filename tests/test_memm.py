from src.ga import decode
from src.memm import MaxEntTagger, MEMMTagger

TOY = [
    (["tôi", "ăn", "cơm"], ["PRON", "VERB", "NOUN"]),
    (["tôi", "đọc", "sách"], ["PRON", "VERB", "NOUN"]),
    (["sách", "hay"], ["NOUN", "ADJ"]),
] * 5


def test_maxent_and_memm_fit_predict():
    for cls in (MaxEntTagger, MEMMTagger):
        m = cls(C=10).fit(TOY)
        assert m.predict(["tôi", "đọc", "cơm"]) == ["PRON", "VERB", "NOUN"]
        assert len(m.predict(["từ lạ"])) == 1
        assert m.predict([]) == []


def test_ga_decode():
    assert decode([1, 0, 0, 0, 0, 0]) == ("word",)

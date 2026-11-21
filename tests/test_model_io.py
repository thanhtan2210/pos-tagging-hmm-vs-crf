import pytest

from src.baseline import MostFrequentTagger
from src.crf import CRFTagger
from src.hmm import HMMTagger
from src.memm import MEMMTagger
from src.model_io import load_model, save_model

TOY = [
    (["tôi", "ăn", "cơm"], ["PRON", "VERB", "NOUN"]),
    (["tôi", "đọc", "sách"], ["PRON", "VERB", "NOUN"]),
    (["sách", "hay"], ["NOUN", "ADJ"]),
] * 5
SENT = ["tôi", "đọc", "cơm", "từ lạ"]


@pytest.mark.parametrize("model", [
    MostFrequentTagger(),
    HMMTagger(alpha=0.1, unk="signature"),
    MEMMTagger(C=10),
    CRFTagger(c1=0.0, c2=0.01, max_iterations=50),
])
def test_save_load_roundtrip(tmp_path, model):
    model.fit(TOY)
    path = tmp_path / "m.joblib"
    save_model(model, path, lang="vi", name="toy", params={})
    loaded, meta = load_model(path)
    assert loaded.predict(SENT) == model.predict(SENT)
    assert meta["name"] == "toy" and meta["class"] == type(model).__name__


def test_load_rejects_other_files(tmp_path):
    import joblib
    path = tmp_path / "x.joblib"
    joblib.dump([1, 2, 3], path)
    with pytest.raises(ValueError):
        load_model(path)

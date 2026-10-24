from src.baseline import MostFrequentTagger
from src.data import read_conllu

SAMPLE = """# sent_id = 1
# text = I don't know.
1	I	I	PRON	PRP	_	4	nsubj	_	_
2-3	don't	_	_	_	_	_	_	_	_
2	do	do	AUX	VBP	_	4	aux	_	_
3	n't	not	PART	RB	_	4	advmod	_	_
4	know	know	VERB	VB	_	0	root	_	SpaceAfter=No
5	.	.	PUNCT	.	_	4	punct	_	_

# sent_id = 2
1	học sinh	học sinh	NOUN	N	_	0	root	_	_
1.1	đi	đi	VERB	V	_	_	_	_	_
"""


def test_read_conllu_skips_multiword_and_empty_nodes(tmp_path):
    path = tmp_path / "sample.conllu"
    path.write_text(SAMPLE, encoding="utf-8")
    sents = read_conllu(path)
    assert sents == [
        (["I", "do", "n't", "know", "."], ["PRON", "AUX", "PART", "VERB", "PUNCT"]),
        (["học sinh"], ["NOUN"]),  # từ tiếng Việt nhiều âm tiết giữ nguyên dấu cách
    ]


def test_baseline_uses_most_frequent_tag():
    train = [(["a", "a", "b"], ["X", "X", "Y"]), (["a"], ["Y"])]
    m = MostFrequentTagger().fit(train)
    assert m.predict(["a", "b", "zzz"]) == ["X", "Y", "X"]

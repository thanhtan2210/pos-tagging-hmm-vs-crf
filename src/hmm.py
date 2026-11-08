"""HMM bigram cho gán nhãn từ loại.

>>> PHẦN NÀY BẠN TỰ CÀI ĐẶT (các chỗ TODO). Chạy `python -m pytest` để kiểm tra. <<<

Ký hiệu (khớp slide Ch.5 Graphical Models, phần HMM):
    pi[i]   = P(t_1 = i)                      xác suất nhãn đầu câu
    A[i, j] = P(t_k = j | t_{k-1} = i)        xác suất chuyển nhãn
    B[i, w] = P(w_k = w | t_k = i)            xác suất phát xạ từ
Mọi tính toán làm trong không gian log để tránh underflow với câu dài
(tích của hàng chục xác suất nhỏ sẽ về 0 khi dùng số thực).
"""
import numpy as np

UNK = "<UNK>"


class HMMTagger:
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # hệ số add-alpha (Laplace khi alpha = 1) smoothing

    def fit(self, sentences):
        self.tags = sorted({t for _, tags in sentences for t in tags})
        self.tag2id = {t: i for i, t in enumerate(self.tags)}
        vocab = sorted({w for words, _ in sentences for w in words}) + [UNK]
        self.word2id = {w: i for i, w in enumerate(vocab)}
        T, V = len(self.tags), len(vocab)

        start = np.zeros(T)
        trans = np.zeros((T, T))
        emit = np.zeros((T, V))

        # TODO(1): duyệt từng câu (words, tags), đếm vào:
        #     start[i]    số câu bắt đầu bằng nhãn i
        #     trans[i, j] số lần nhãn j đứng ngay sau nhãn i
        #     emit[i, w]  số lần từ w mang nhãn i
        #

        # TODO(2): cộng self.alpha vào mỗi ô, chuẩn hóa để mỗi hàng có tổng = 1,
        #     rồi lấy log và lưu vào:
        #     self.log_pi  shape (T,)
        #     self.log_A   shape (T, T)
        #     self.log_B   shape (T, V)
        #
        # Ghi chú: cột UNK của emit toàn 0, sau smoothing mỗi nhãn i cho UNK
        # xác suất alpha / (count(i) + alpha * V). Đây là cách xử lý từ lạ
        # đơn giản nhất; RQ2 sẽ so sánh với cách khác (vd. coi từ chỉ xuất
        # hiện 1 lần trong train là UNK).
        raise NotImplementedError("TODO(1), TODO(2) trong HMMTagger.fit")
        return self

    def predict(self, words):
        ids = [self.word2id.get(w, self.word2id[UNK]) for w in words]
        path = viterbi(self.log_pi, self.log_A, self.log_B[:, ids])
        return [self.tags[i] for i in path]


def viterbi(log_pi, log_A, log_emit):
    """Tìm chuỗi nhãn có xác suất hợp cao nhất.

    log_pi   : (T,)    log P(t_1 = i)
    log_A    : (T, T)  log P(t_k = j | t_{k-1} = i)
    log_emit : (T, n)  log_emit[i, k] = log P(w_k | t_k = i), n là độ dài câu
    Trả về list gồm n chỉ số nhãn.
    """
    # TODO(3): quy hoạch động
    #     delta[0, j] = log_pi[j] + log_emit[j, 0]
    #     delta[k, j] = max_i (delta[k-1, i] + log_A[i, j]) + log_emit[j, k]
    #     back[k, j]  = argmax_i của biểu thức trên
    # rồi truy vết ngược từ argmax_j delta[n-1, j].
    # Gợi ý: có thể vector hóa vòng lặp theo i bằng broadcasting
    #     delta[k-1][:, None] + log_A   -> ma trận (T, T)
    raise NotImplementedError("TODO(3) trong viterbi")

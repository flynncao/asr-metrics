import re
import string

def preprocess(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', '', text).strip()
    return text

def cer(ref, hyp):
    m, n = len(ref), len(hyp)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + (0 if ref[i-1] == hyp[j-1] else 1)
            )
    return dp[m][n] / m if m > 0 else 0.0

with open('./mando2/ground truth.txt', 'r', encoding='utf-8') as f:
    ref = preprocess(f.read())
with open('./mando2/wav2vec2.txt', 'r', encoding='utf-8') as f:
    hyp = preprocess(f.read())

print(f"CER: {cer(ref, hyp) * 100:.2f}%")

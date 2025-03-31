import re
import string

def preprocess(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text.split()

def levenshtein(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
    return dp[m][n]

def mer(ref_words, hyp_words):
    total_errors = 0
    ref_len = sum(len(word) for word in ref_words)
    m, n = len(ref_words), len(hyp_words)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = sum(len(ref_words[k]) for k in range(i))
    for j in range(n + 1):
        dp[0][j] = sum(len(hyp_words[k]) for k in range(j))
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            sub_cost = levenshtein(ref_words[i-1], hyp_words[j-1])
            dp[i][j] = min(
                dp[i-1][j] + len(ref_words[i-1]),
                dp[i][j-1] + len(hyp_words[j-1]),
                dp[i-1][j-1] + sub_cost
            )
    return dp[m][n] / ref_len if ref_len > 0 else 0.0

with open('./cs/ground truth.txt', 'r', encoding='utf-8') as f:
    ref = preprocess(f.read())
with open('./cs/phi4.txt', 'r', encoding='utf-8') as f:
    hyp = preprocess(f.read())

print(f"MER: {mer(ref, hyp) * 100:.2f}%")

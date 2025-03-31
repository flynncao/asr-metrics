import re
import string

def preprocess(text):
		# remove all punctuations
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def wer(ref, hyp):
    ref_words = ref.split()
    hyp_words = hyp.split()
    m, n = len(ref_words), len(hyp_words)
    print('number in ref_words', m)
    print('number in hyp_words', n)
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
                dp[i-1][j-1] + (0 if ref_words[i-1] == hyp_words[j-1] else 1)
            )
    return dp[m][n] / m if m > 0 else 0.0

with open('./mando2/ground truth.txt', 'r', encoding='utf-8' ) as f:
    ref = preprocess(f.read())
with open('./mando2/whisper large-v3-webui.txt', 'r', encoding='utf-8') as f:
    hyp = preprocess(f.read())

print(f"WER: {wer(ref, hyp) * 100:.2f}%")

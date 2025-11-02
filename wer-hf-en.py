from evaluate import load
import re
import string
import jieba

all_punctuation = string.punctuation + '\ufeff'  


def preprocess(text, lang='', preciseSplitting=False):
    # Remove punctuation and extra spaces
    print(text)
    text = text.translate(str.maketrans('', '', all_punctuation.replace('.', '')))
    text = re.sub(r'\s+', ' ', text).strip()
    # split the text into words with jieba
    if preciseSplitting:
        if lang == 'cn':
            text = ' '.join(jieba.cut(text, cut_all=False))
    return text

# Examples
# ref_text = "就直走 前面你看人多的地方吗 嗯 嗯 摆摊的那就有 你好 小姐姐 我请问你一下 你知道这个延安三路地铁站 是怎么个走法吗"
# hyp_text = "就直走前面 你看人多的地方吗 嗯 摆摊的那就有 你好 夏小姐 我请问你一下 你知道延安三路 地铁站是怎么个总坊"


ref_path = './en1/ground truth.txt'
hyp_path = './en1/whisper.txt'

with open(ref_path, 'r', encoding='utf-8' ) as f:
    ref = f.read()
with open(hyp_path, 'r', encoding='utf-8') as f:
    hyp = f.read()


if 'mando' in ref_path or 'cs' in ref_path:
    ref_sentences = preprocess(ref, lang='cn', preciseSplitting=True).split()
    hyp_sentences = preprocess(hyp, lang='cn', preciseSplitting=True).split()
else:
	ref_sentences = [s for s in preprocess(ref, preciseSplitting=True).split('.') if s]
	hyp_sentences = [s for s in preprocess(hyp, preciseSplitting=True).split('.') if s]

if len(ref_sentences) > len(hyp_sentences):
    for i in range(len(ref_sentences) - len(hyp_sentences)):
        hyp_sentences.append(' ')
elif len(hyp_sentences) > len(ref_sentences):
    for i in range(len(hyp_sentences) - len(ref_sentences)):
        ref_sentences.append(' ')

print('reference: ', ref_sentences)
print('hypothesis: ', hyp_sentences)
# Calculate WER
wer = load("wer")
wer_score = wer.compute(predictions=hyp_sentences, references=ref_sentences)
print(f"TOTAL WER: {wer_score:.2%}")



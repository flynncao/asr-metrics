import re
import string
import jieba

ref_path = './mando2/ground truth.txt'
hyp_path = './mando2/whisper large-v3-webui.txt'

chinese_punctuation = '。，、；：「」『』（）《》〈〉【】〔〕〖〗〘〙〚〛〜～’‘”“＂＇´﹃﹄…'
all_punctuation = string.punctuation + chinese_punctuation + '\ufeff'


# Remove all modal particles in Chinese
modal_particles = ['嗯', '啊', '呀', '哦', '嘛', '吧', '呢', '呐', '呗', '唉', '哈']


def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', all_punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    for particle in modal_particles:
        text = text.replace(particle, '')
    return text.split()


def count_errors(ref, hyp):
    i = j = errors = 0
    while i < len(ref) and j < len(hyp):
        if ref[i] == hyp[j]:
            i += 1
            j += 1
        else:
            if (i + 1 < len(ref) and ref[i + 1] == hyp[j]):
                errors += 1
                i += 1
            elif (j + 1 < len(hyp) and hyp[j + 1] == ref[i]):
                errors += 1
                j += 1
            else:
                errors += 1
                i += 1
                j += 1

    errors += abs((len(ref) - i) - (len(hyp) - j))
    return errors


def calculate_wer(ref_sents, hyp_sents, lang='' ):
    total_errors = 0
    total_ref_words = 0

    for ref, hyp in zip(ref_sents, hyp_sents):
        ref_words = list(jieba.cut(ref, cut_all=False))
        hyp_words = list(jieba.cut(hyp, cut_all=False))
        print('ref_words: ', ref_words)
        print('hyp_words: ', hyp_words)
        errors = count_errors(ref_words, hyp_words)
        total_errors += errors
        total_ref_words += len(ref_words)

    return total_errors / total_ref_words if total_ref_words > 0 else 0


# Input data
exp_ref_sentences = preprocess("就直走\n前面你看人多的地方吗\n嗯\n嗯\n摆摊的那就有\n你好\n小姐姐\n我请问你一下\n你知道这个延安三路地铁站\n是怎么个走法吗")
exp_hyp_sentences = preprocess("就直走前面\n你看人多的地方吗\n嗯\n摆摊的那就有\n你好\n夏小姐\n我请问你一下\n你知道延安三路\n地铁站是怎么个总坊")
wer = calculate_wer(exp_ref_sentences, exp_hyp_sentences, lang='cn')
print(f"WER: {wer:.2%}")


with open(ref_path, 'r', encoding='utf-8' ) as f:
    ref = f.read()
with open(hyp_path, 'r', encoding='utf-8') as f:
    hyp = f.read()


ref_sentences = preprocess(ref)
hyp_sentences = preprocess(hyp)

print('reference: ', ref_sentences)
print('hypothesis: ', hyp_sentences)

# Calculate WER
wer = calculate_wer(ref_sentences, hyp_sentences)
print(f"WER: {wer * 100:.2f}%")




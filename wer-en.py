import re
import string

ref_path = './en1/ground truth.txt'
hyp_path = './en1/whisper.txt'

# English punctuation (standard punctuation)
all_punctuation = string.punctuation + '\ufeff'


def preprocess(text):
    # Convert to lowercase and remove all punctuation
    text = text.lower()
    text = text.translate(str.maketrans('', '', all_punctuation))
    # Normalize spaces (collapse multiple spaces into one)
    text = re.sub(r'\s+', ' ', text).strip()
    # Split the text into words
    return text.split('\n')


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


def calculate_wer(ref_sents, hyp_sents):
    total_errors = 0
    total_ref_words = 0

    for ref, hyp in zip(ref_sents, hyp_sents):
        ref_words = ref.split()
        hyp_words = hyp.split()
        print('ref_words: ', ref_words)
        print('hyp_words: ', hyp_words)
        errors = count_errors(ref_words, hyp_words)
        total_errors += errors
        total_ref_words += len(ref_words)

    return total_errors / total_ref_words if total_ref_words > 0 else 0


# Input data (English example)
exp_ref_sentences = preprocess("Go straight ahead. You will see a crowded place. Hmm. Hmm, the street vendors are there. Hello, miss.")
exp_hyp_sentences = preprocess("Go straight ahead, you will see a crowded place. Hmm, the street vendors are there. Hello, Summer.")

wer = calculate_wer(exp_ref_sentences, exp_hyp_sentences)
print(f"WER: {wer:.2%}")


#You can also load your files for English WER calculation
with open(ref_path, 'r', encoding='utf-8') as f:
    ref = f.read()
with open(hyp_path, 'r', encoding='utf-8') as f:
    hyp = f.read()

ref_sentences = preprocess(ref)
hyp_sentences = preprocess(hyp)

print('Reference: ', ref_sentences)
print('Hypothesis: ', hyp_sentences)

# Calculate WER
wer = calculate_wer(ref_sentences, hyp_sentences)
print(f"WER: {wer * 100:.2f}%")

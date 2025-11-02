import re
import string


'''
If the input text contains many sentence fragment insertions, the WER may be higher than expected.
'''


# English punctuation (standard punctuation)
all_punctuation = (string.punctuation + '\ufeff').replace('.', '')


def preprocess(text):
		# Convert to lowercase and remove all punctuation
		text = text.lower()
		text = text.translate(str.maketrans('', '', all_punctuation))
		# Normalize spaces (collapse multiple spaces into one)
		text = re.sub(r'\s+', ' ', text).strip()
		# Split the text into words
		# Split by periods first, then by commas, and flatten the result
		sentences = text.replace('\n', '.').split('.')
		return sentences
		# words = []
		# for sentence in sentences:
		# 	words.extend(sentence.split(','))
		# # Filter out empty strings and strip whitespace
		# return [word.strip() for word in words if word.strip()]


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
      errors = count_errors(ref_words, hyp_words)
      total_errors += errors
      total_ref_words += len(ref_words)

    return total_errors / total_ref_words if total_ref_words > 0 else 0


# # Input data (English example)
# exp_ref_sentences = preprocess("Go straight ahead. You will see a crowded place. Hmm. Hmm, the street vendors are there. Hello, miss.")
# exp_hyp_sentences = preprocess("Go straight ahead, you will see a crowded place. Hmm, the street vendors are there. Hello, Summer.")

# wer = calculate_wer(exp_ref_sentences, exp_hyp_sentences)
# print(f"WER: {wer:.2%}")


def wer(ref, hyp):
		# Preprocess the sentences, remove punctuation, and convert to lowercase
		ref_sentences = preprocess(ref)
		hyp_sentences = preprocess(hyp)
		print('ref...')
		print(ref_sentences)
		print(hyp_sentences)
		# Calculate WER
		wer_result = calculate_wer(ref_sentences, hyp_sentences)
		return '{0:.2f}%'.format(wer_result * 100)


def main():
	ref_path = './en1/ground truth.txt'
	hyp_path = './en1/whisper.txt'
	with open(ref_path, 'r', encoding='utf-8') as f:
		ref = f.read()
	with open(hyp_path, 'r', encoding='utf-8') as f:
		hyp = f.read()
	# Calculate WER
	print(wer(ref, hyp))
	
	
if __name__ == '__main__':
		main()

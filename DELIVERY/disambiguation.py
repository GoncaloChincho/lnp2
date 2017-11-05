#python disambiguation.py [unigrams_file] [bigrams_file] [param_file] [sentences_file]
import sys
import math

def unigram_probability(cw, N, V):
    return math.log(cw/(N + V))

def bigram_probability(cw12, cw1, V):
    return math.log(cw12/(cw1 + V))

if(len(sys.argv) != 5):
    print('Usage: python disambiguation.py [unigrams_file] [bigrams_file] [param_file] [sentences_file]')
    quit()
else:
    unigrams_file = open(sys.argv[1])
    bigrams_file = open(sys.argv[2])
    param_file = open(sys.argv[3])
    sentences_file = open(sys.argv[4])

#input unigram and bigram files contain c* count

unigrams_filter = (unigrams_file.read()).split('\n')
unigrams = {}
for entry1 in unigrams_filter:
    if(not entry1):
        break #EOF
    unigrams[entry1.split()[0]] = int(entry1.split()[1])
vocabulary = len(unigrams)
n_count = sum(unigrams.values())

bigrams_filter = (bigrams_file.read()).split('\n')
bigrams = {}
for entry2 in bigrams_filter:
    if(not entry2):
        break #EOF
    bigrams[(entry2.split()[0], entry2.split()[1])] = entry2.split()[2]


param_filter = (param_file.read()).split('\n')
ambiguous = param_filter[0]
lemma1 = param_filter[1].split()[0]
lemma2 = param_filter[1].split()[1]

param_file.close()

sentences_filter = (sentences_file.read()).split('\n')
start_token = unigrams["<s>"]
end_token = unigrams["</s>"]

start_token_prob = unigram_probability(start_token, n_count, vocabulary)
end_token_prob = unigram_probability(end_token, n_count, vocabulary)
c = 0
for sentence in sentences_filter:
    if(not sentence):
        break #EOF
    words = sentence.split()
    prob = [1, 1, 1, 1]
    for i in range(0, len(words)):
        if(words[i] == ambiguous):
            prob[0] *= unigram_probability(unigrams[lemma1], n_count, vocabulary)
            prob[1] *= unigram_probability(unigrams[lemma2], n_count, vocabulary)

            if(i == 0):
                prob[0] += start_token_prob
                prob[1] += start_token_prob
                prob[2] += bigram_probability(bigrams[("<s>", lemma1)], start_token, vocabulary)
                prob[3] += bigram_probability(bigrams[("<s>", lemma2)], start_token, vocabulary)

            if(i == len(words)-1):
                prob[0] += uni_prob
                prob[1] += uni_prob
                prob[2] += bigram_probability(bigrams[("</s>", lemma1)], start_token, vocabulary)
                prob[3] += bigram_probability(bigrams[("</s>", lemma2)], start_token, vocabulary)
                break

            if(words[i+1] not in unigrams):
                count_intersect1 = 1
                count_intersect2 = 1
            else:
                count_intersect1 = bigrams[(lemma1, words[i+1])]
                count_intersect2 = bigrams[(lemma2, words[i+1])]

            prob[2] += bigram_probability(count_intersect1, unigrams[lemma1], vocabulary)
            prob[3] += bigram_probability(count_intersect2, unigrams[lemma2], vocabulary)

        else:
            if(words[i] in unigrams):
                prob_aux = [0, 0, 0, 0]
                prob[0] += unigram_probability(unigrams[words[i]], n_count, vocabulary)
                prob[1] += unigram_probability(unigrams[words[i]], n_count, vocabulary)

                if(i == 0):
                    prob_aux[0] = start_token_prob
                    prob_aux[1] = bigram_probability(bigrams[("<s>", words[i])], start_token, vocabulary)
                    prob[0] += prob_aux[0]
                    prob[1] += prob_aux[0]
                    prob[2] += prob_aux[1]
                    prob[3] += prob_aux[1]

                if(i == len(words)-1):
                    prob_aux[2] = end_token_prob
                    prob_aux[3] = bigram_probability(bigrams[("</s>", words[i])], start_token, vocabulary)
                    prob[0] += prob_aux[2]
                    prob[1] += prob_aux[2]
                    prob[2] += prob_aux[3]
                    prob[3] += prob_aux[3]
                    break

                if(words[i+1] not in unigrams):
                    count_intersect1 = 1
                    count_intersect2 = 1
                elif(words[i+1] == ambiguous):
                    count_intersect1 = bigrams[(words[i], lemma1)]
                    count_intersect2 = bigrams[(words[i], lemma2)]
                else:
                    count_intersect1 = bigrams[(words[i], words[i+1])]
                    count_intersect2 = bigrams[(words[i], words[i+1])]

                prob[2] += bigram_probability(count_intersect1, unigrams[words[i]], vocabulary)
                prob[3] += bigram_probability(count_intersect2, unigrams[words[i]], vocabulary)

            else:
                prob[0] += unigram_probability(1, n_count, vocabulary)
                prob[1] += unigram_probability(1, n_count, vocabulary)
                prob[2] += bigram_probability(1, 0, vocabulary)
                prob[3] += bigram_probability(1, 0, vocabulary)

    print("Sentence index " + c)
    c += 1
    print("Unigram probability " + lemma1 + ":\t")
    print("%5f" % prob[0])
    print("\nUnigram probability " + lemma2 + ":\t")
    print("%5f" % prob[1])
    print("\nBigram probability " + lemma1 + ":\t")
    print("%5f" % prob[2])
    print("\nBigram probability " + lemma2 + ":\t")
    print("%5f" % prob[3])


# coding: utf-8
import re
import sys

valid_words = ['aposta','forem']

if(len(sys.argv) != 2):
    print('Usage: python outToFinal.py (aposta|forem)')
    quit()
elif(sys.argv[1] not in valid_words):
    print('Not a valid word, choose aposta or forem')
    quit()

word = sys.argv[1]

if word == 'aposta':
    final_filename = r'apostaStuff\apostaAnotado.final'
    out_path = r'apostaStuff\apostaAnotado.out'
else:
    final_filename = r'foremIrSerStuff\foremAnotado.final'
    out_path = r'foremIrSerStuff\foremAnotado.out'


with open(out_path,'r',encoding='utf-8') as file:
    read = file.read()
file_lines = read.split('\n')

#filter out the dirty dirty sentences
final_sentences = []
final_tags = []

for line in file_lines:
    split_line = line.split('\t')
    tag = split_line[0]
    sentence = split_line[1]
    if not (tag.count('n-é-verbo') or (sentence.count(word) > 1) or tag.count('#') or tag.count('?')):
        final_sentences.append(sentence)
        final_tags.append(tag)

#replace by the lemma
for i in range(len(final_tags)):
    final_sentences[i] = re.sub('\\b' + word + '\\b',final_tags[i],final_sentences[i])


#write


file = open(final_filename,'w')

for sentence in final_sentences:
    file.write('<s> ' + sentence + '</s> \n')

file.close()
print('The deed is done.')

import spacy
from nameparser.parser import HumanName

def name_decoder(name):
    sum = 0
    for c in name:
        sum += ord(c)
    return "{0:b}".format(sum)

def find_longest_consecutive(sequence):
    sum, res = 0,0
    for i in sequence:
        if i == '0':
            sum += 1
        else:
            sum = 0
        if sum > res:
            res = sum
    return res



def get_human_names(text):
    en = spacy.load('en')

    sents = en(text)
    person_list = []
    for word in sents.ents:
        if word.label_ == 'PERSON':
            person_list.append(str(word).replace('\n',''))




    result = []

    for name in person_list:

        try:

            first_last = str(HumanName(name).first).replace(' ','') + ' ' + str(HumanName(name).last).replace(' ','')

            result.append(first_last)
        except:
            print('error')


    return result




import warnings
warnings.filterwarnings("ignore")

import os
import re
import nltk
from nltk.internals import find_jars_within_path
from nltk.parse.stanford import StanfordDependencyParser
from nltk.internals import find_jars_within_path
from nltk.tag import StanfordPOSTagger
from practnlptools.tools import Annotator
import os.path as osp
from nltk.parse import stanford
from textblob import TextBlob
import sys
import random
from quantulum import parser as qp
import matplotlib


datadir = osp.join('/Users/carlosgonzalezoliver/Projects/NLPlotlib/roman_data')
os.environ['STANFORD_PARSER'] = osp.join(datadir, 'stanford/stanford-parser.jar')
os.environ['STANFORD_MODELS'] = osp.join(datadir, 'stanford/stanford-parser-3.9.1-models.jar')
os.environ['CLASSPATH'] = osp.join(datadir, "stanford_data")
def get_type(text,word):
    #annotator=Annotator()
    #pos = annotator.getAnnotations(text)["pos"]
    st = StanfordPOSTagger(osp.join(datadir, 'stanford_pos/models/english-bidirectional-distsim.tagger'),\
	osp.join(datadir, "stanford_pos/stanford-postagger.jar"))
    #stanford_dir = st._stanford_jar.rpartition('/')[0]
    #stanford_jars = find_jars_within_path(stanford_dir)
    #st.stanford_jar = ':'.join(stanford_jars)
    #result = dep_parser.raw_parse(text)
    pos = st.tag(text)
    for i in pos:
        if i[0]==word:
            return i[1]
    return None

def get_action_verb_from_string(text):
    blob = TextBlob(text)
    # print(blob)
    noun_phrases = blob.noun_phrases

    verbs = list()
    for word, tag in blob.tags:
        # print(word)
        # print(tag)
        if tag == 'VB':
            verbs.append(word.lemmatize())
    return verbs

def get_word_dependencies(text):
    dependencies = {}
    dep_parser=StanfordDependencyParser(model_path=osp.join(datadir, "stanford_data/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"),java_options="-mx4g -XX:-UseGCOverheadLimit")
    st = StanfordPOSTagger(osp.join(datadir, "stanford_pos/stanford-postagger-3.9.1.jar"),\
		osp.join(datadir, 'stanford_pos/models/english-bidirectional-distsim.tagger'), java_options='-mx4g, XX:-UseGCOverheadLimit')
    stanford_dir = st._stanford_jar.rpartition('/')[0]
    stanford_jars = find_jars_within_path(stanford_dir)
    st.stanford_jar = ':'.join(stanford_jars)
    result = dep_parser.raw_parse(text)
    dep = result.__next__()
    #print(list(dep.triples()))
    for i in list(dep.triples()):
        w1 = i[0][0]
        w2 = i[2][0]
        if w1 in dependencies:
            dependencies[w1].append((w2,i[1]))
        else:
            dependencies[w1] = [(w2,i[1])]
    #print(dependencies)
    return dependencies

def get_complement_to_verb(text,verb):
    complement = []
    dependencies = get_word_dependencies(text)
    if verb not in dependencies:
        return []
    for i in dependencies[verb]:
        complement.append(i[0])
    for c in complement:

        if c not in dependencies:
            continue
        comp_of_comp = dependencies[c]
        for d in comp_of_comp:
            #print(get_type(text,d))
            #print("D",d)
            if "subj" in d[1]:
                complement.append(d[0])

            if "conj" in d:
                complement.append(d[0])
            if "nmod" in d:
                complement.append(d[0])

    #print(complement)
    return complement

def find_number(text):
    numbers = []
    this_number = ""
    for ind,i in enumerate(text):
        if i.isdigit()==True:
            this_number = this_number+i
            if ind+1 == len(text):
                numbers.append(this_number)
                return numbers
            elif text[ind+1].isdigit()==False:
                numbers.append(this_number)
                this_number=""
    return numbers
def get_colors():
    colors = []
    for name,hex in matplotlib.colors.cnames.items():
        colors.append(name)
    return colors

def comp_to_val(comp,values):
    colors = get_colors()
    for i in comp:
        if i in colors:
            values.append(i)
            comp.remove(i)
    return(comp,values)


def get_action_from_sentence(text):
    if "\"" not in text:
        words = nltk.tokenize.word_tokenize(text)

        full_text = text
        regex = re.compile('[^0-9a-zA-Z !?]')
        text=regex.sub('', text)
        #print(text)
        numbers = find_number(text)
        #print(numbers)
        for num in numbers:
            text = text.replace(num,"many")
        #print(text)
        verbs = get_action_verb_from_string(text)
        if verbs == []:
            verbs = [words[0]]
        verb = verbs[0]
        complement = get_complement_to_verb(text,verb)
        value = qp.parse(full_text)
        #print(type(value))
        #print(value)
        #value = ",".join(value)
        #print(type(value))
        if "dimensionless" in value:
            value= value.surface
        else:
            value = [value[i] for i in range(len(value))]
        order = nltk.tokenize.word_tokenize(text)

        complement.sort(key=lambda x: order.index(x))
        if "many" in complement:
            complement.remove("many")
        complement, value = comp_to_val(complement,value)
        # print("INPUT: ", text)
        # print("Action : ", verb, complement)
        # print("Quantity : ", value)
        # print("-------------------------------------------")
    else:

        value=text.split("\"")[1]
        words = nltk.tokenize.word_tokenize(text)
        full_text = text
        text = text.replace(value,"")
        regex = re.compile('[^a-zA-Z !?]')
        text=regex.sub('', text)
        numbers = find_number(text)
        for num in numbers:
            text = text.replace(num,"many")
        verbs = get_action_verb_from_string(text)
        if verbs == []:
            verbs = [words[0]]
        verb = verbs[0]
        complement = get_complement_to_verb(text,verb)
        #value = qp.parse(text)
        order = nltk.tokenize.word_tokenize(text)

        complement.sort(key=lambda x: order.index(x))
        if "many" in complement:
            complement.remove("many")
        comp,value = comp_to_val(complement,value)
        # print("INPUT: ", text)
        # print("Action : ", verb, complement)
        # print("Quantity : ", value)
        # print("-------------------------------------------")
    return([verb,complement,value])
if __name__ == "__main__":
	t1 = "Make a scatter plot from this data file."
	t2 = "Make the title bigger and blue."
	t3 = """Add a title "Number of pumpkins per second" to the x-axis."""
	t4 = "Remove 50% of the ticks on the y-axis. "
	t5 = "Make the y-axis go from 0 to 1."
	#get_action_from_sentence(t1)
	#get_action_from_sentence(t2)
	#get_action_from_sentence(t3)
	#print(get_action_from_sentence(t4))
	#get_action_from_sentence(t5)

	print(get_action_from_sentence("Draw a scatter plot of test.csv"))

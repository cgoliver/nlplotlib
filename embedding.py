import numpy as np
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors



def convert():
    #convert to glove format
    glove_input_file = 'Data/glove.6B/glove.6B.50d.txt'
    word2vec_output_file = 'Data/glove.6B.50d.txt.word2vec'
    glove2word2vec(glove_input_file, word2vec_output_file)

def model_load(modelpath='Data/glove.6B.50d.txt.word2vec'):
    return KeyedVectors.load_word2vec_format(modelpath, binary=False)
    
def embed(word, model):
    return model[word]

def sentence_embed(model, sentence):
    """
    Embed sentence as mean of word embeddings.
    """
    vec = []
    for w in sentence:
        try:
            vec.append(model[w]) 
        except KeyError:
            print(f"word {w} not in vocab")
            continue
    #if no embeddings found
    if len(vec) == 0:
        return np.zeros((50))
    else:
        return np.mean(vec, axis=0)
    
if __name__ == "__main__":
    words = ['plot', 'axis']
    model = model_load()
    # print(model.wv.vocab)
    # model = model_load()
    print(sentence_embed(model, words))

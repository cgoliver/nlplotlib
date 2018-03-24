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
    # calculate: (king - man) + woman = ?
    result = model.most_similar(positive=['woman', 'king'], negative=['man'],\
        topn=1)
    try:
        print(model[word])
    except KeyError:
        print("word not in vocabulary")
    # print(result)

def sentence_embed(model, sentence):
    """
    Embed sentence as mean of word embeddings.
    """
    vec = []
    for w in words:
        vec.append(embed(w, model))
    meaned = np.mean(vec, axis=0)
    return meaned
    
if __name__ == "__main__":
    words = ['carlos', 'roman', 'plot', 'axis']
    model = model_load()

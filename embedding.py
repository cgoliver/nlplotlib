from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors



def convert():
    #convert to glove format
    glove_input_file = 'Data/glove.6B/glove.6B.50d.txt'
    word2vec_output_file = 'Data/glove.6B.50d.txt.word2vec'
    glove2word2vec(glove_input_file, word2vec_output_file)

def embed(modelpath='Data/glove.6B.50d.txt.word2vec'):
    model = KeyedVectors.load_word2vec_format(modelpath, binary=False)
    # calculate: (king - man) + woman = ?
    result = model.most_similar(positive=['woman', 'king'], negative=['man'],\
        topn=1)
    try:
        print(model['roman'])
    except KeyError:
        print("word not in vocabulary")
    # print(result)


if __name__ == "__main__":
    embed()

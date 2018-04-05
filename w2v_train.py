import pickle
from gensim.models import Word2Vec

def embed_train(sentences):
    model = Word2Vec(sentences, size=15,window=2, min_count=1)
    model.wv.save_word2vec_format('Data/model_SO_w2v_15d.word2vec')
    print(model)
    return model

if __name__ == "__main__":
    sentences = pickle.load(open("Data/sentences_clean.pickle", "rb"))
    print("training word2vec model")
    embed_train(sentences)
    pass

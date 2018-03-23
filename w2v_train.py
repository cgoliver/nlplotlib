import pickle


from gensim.models import Word2Vec

def embed_train(sentences):
    model = Word2Vec(sentences, size=50,window=2, min_count=1)
    model.save('model_w2_50d.bin')
    print(model)
    return model

if __name__ == "__main__":
    sentences = pickle.load(open("sentences_clean.pickle", "rb"))
    print("training word2vec model")
    embed_train(sentences)
    pass

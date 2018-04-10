from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot

def load_model(modelpath):
    return Word2Vec.load(modelpath)


def pca(model):
    num_words = 15 
    X = model[model.wv.vocab][:num_words]
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    pyplot.scatter(result[:, 0], result[:, 1])
    words = list(model.wv.vocab)[:num_words]
    for i, word in enumerate(words):
        pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    pyplot.savefig("embed_SO_pca.png", format="png")
    pyplot.show()

if __name__ == "__main__":
    model = load_model('Data/model_SO_w2v_15d.bin')
    pca(model)

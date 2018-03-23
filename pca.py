from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot

def load_model(modelpath):
    return Word2Vec.load(modelpath)


def pca(model):
    X = model[model.wv.vocab][:10]
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    pyplot.scatter(result[:, 0], result[:, 1])
    words = list(model.wv.vocab)[:10]
    for i, word in enumerate(words):
        pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    pyplot.savefig("embed_pca.pdf", format="pdf")
    # pyplot.show()

if __name__ == "__main__":
    model = load_model('Data/model_w2_50d.bin')
    pca(model)

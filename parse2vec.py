from gensim.models import Word2Vec 
sentences = [['first', 'sentence'], ['second', 'sentence']]
model = Word2Vec(sentences, min_count=1)

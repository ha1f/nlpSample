#coding: utf-8

from gensim.models.word2vec import Word2Vec

class Word2VecService(object):
    def __init__(self):
        model_path = './latest-ja-word2vec-gensim-model/word2vec.gensim.model'
        self.model = Word2Vec.load(model_path)
    def similarity(self, w1, w2):
        return self.model.similarity(w1, w2)

if __name__ == '__main__':
    service = Word2VecService()
    print(service.similarity("コアラ", "ゴリラ"))
    print(service.similarity("コアラ", "スマホ"))
#coding: utf-8

from gensim.models.word2vec import Word2Vec
import gensim
import MeCab

class Word2VecService(object):
    def __init__(self):
        model_path = './latest-ja-word2vec-gensim-model/word2vec.gensim.model'
        self.model = Word2Vec.load(model_path)
    def similarity(self, w1, w2):
        return self.model.similarity(w1, w2)

class TaggerService(object):
    def __init__(self):
        self.tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    def parse(self, text):
        return self.tagger.parse(text)

if __name__ == '__main__':
    service = TaggerService()
    print(service.parse("アイドルマスター・シンデレラガールズで遊んだよ！"))

    wService = Word2VecService()
    print(wService.similarity("コアラ", "ゴリラ"))
    print(wService.similarity("コアラ", "スマホ"))

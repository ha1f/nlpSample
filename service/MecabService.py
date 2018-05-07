#coding: utf-8

import MeCab

class MecabService(object):
    def __init__(self):
        self.tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    def parse(self, text):
        return self.tagger.parse(text)

if __name__ == '__main__':
    service = MecabService()
    print(service.parse("Rの法則をみた"))
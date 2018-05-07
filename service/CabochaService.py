#coding: utf-8

import CaboCha

class CabochaService(object):
    def __init__(self):
        self.parser = CaboCha.Parser()
    def parse_to_string(self, text):
        return self.parser.parseToString(text)
    

if __name__ == '__main__':
    service = CabochaService()
    print(service.parse_to_string("Rの法則をみた"))
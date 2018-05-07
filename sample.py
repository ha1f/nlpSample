#coding: utf-8

from service.CabochaService import CabochaService
from service.MecabService import MecabService
from service.Word2VecService import Word2VecService

if __name__ == '__main__':
    service = MecabService()
    print(service.parse("今日はいい天気ですね"))
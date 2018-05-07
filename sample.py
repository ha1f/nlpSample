#coding: utf-8

import os, sys
sys.path.append("{}/service".format(os.getcwd()))

from service.CabochaService import CabochaService
from service.MecabService import MecabService
from service.Word2VecService import Word2VecService
from service.JumanApi import JumanApi

if __name__ == '__main__':
    service = MecabService()
    print(service.parse("今日はいい天気ですね"))

    print([mrph.midasi for mrph in JumanApi.analysis("今日はいい天気ですね").mrph_list()])
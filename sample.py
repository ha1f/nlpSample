#coding: utf-8

import os, sys
sys.path.append("{}/service".format(os.getcwd()))

from service.CabochaService import CabochaService
from service.MecabService import MecabService
from service.Word2VecService import Word2VecService
from service.JumanService import JumanService
from service.KnpService import KnpService

if __name__ == '__main__':
    service = MecabService()
    print(service.parse("今日はいい天気ですね"))

    jumanService = JumanService()
    print([mrph.midasi for mrph in jumanService.analysis("今日はいい天気ですね").mrph_list()])
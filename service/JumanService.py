#coding: utf-8

from pyknp import Juman
from JumanKnpUtil import JumanKnpUtil

class JumanService(object):
    def __init__(self):
        self.__juman = Juman()
    def analysis(self, string):
        formattedString = JumanKnpUtil.format_input_string(string)
        return self.__juman.analysis(formattedString)

if __name__ == '__main__':
    service = JumanService()
    print([mrph.midasi for mrph in service.analysis("今日はいい天気ですね").mrph_list()])

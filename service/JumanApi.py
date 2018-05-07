#coding: utf-8

from pyknp import Juman
from JumanKnpUtil import JumanKnpUtil

class JumanApi(object):
    __juman = Juman()
    @staticmethod
    def analysis(string):
        formattedString = JumanKnpUtil.format_string(string)
        return JumanApi.__juman.analysis(formattedString)

if __name__ == '__main__':
    print([mrph.midasi for mrph in JumanApi.analysis("今日はいい天気ですね").mrph_list()])

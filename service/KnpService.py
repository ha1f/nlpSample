#coding: utf-8

from pyknp import KNP
from JumanKnpUtil import JumanKnpUtil

"""
Bunsetsu
    mrph_list(): MList
    tag_list(): TList
    parent_id: Int, -1ならなし
    parent: Bunsetsu
    children: [Bunsetsu]
    dpndtype: String, 係り受けタイプ
    fstring: String, 素性タグ
    _pstring: String
    bnst_id: Int
    repname: Int
"""

class KnpService(object):
    MARK_EOS = "EOS"
    def __init__(self):
        self.__knp = KNP()
    def parse(self, string):
        formatted_string = JumanKnpUtil.format_input_string(string)
        return self.__knp.parse(formatted_string)
    def parse_all(self, strings):
        return [self.parse(string) for string in strings.split("\n")]
    def result(self, string_iterator):
        results = []
        data = ""
        for line in string_iterator:
            data += line
            if line.strip() == KnpService.MARK_EOS:
                results.append(self.__knp.result(data))
                data=""
        return results
    def load_with_handler(self, string_iterator, handler):
        data = ""
        for line in string_iterator:
            data += line
            if line.strip() == KnpService.MARK_EOS:
                # 応急処置 (出力がまともに出ていない or 文が長すぎるなどが原因で格解析ができなくて構文解析だけが行われた場合をスキップ)
                if not(JumanKnpUtil.is_match_partly(r"\n\* \d+ ", data)) and not(JumanKnpUtil.is_match_partly(r"Fell back to", data)):
                    handler(self.__knp.result(data))
                data=""
        return
    def load_from_file_with_handler(self, filepath, handler):
        with open(filepath, "r") as f:
            results = self.load_with_handler(iter(f.readline, ""), handler)
        return results
    def load_from_file(self, filepath):
        with open(filepath, "r") as f:
            results = self.result(iter(f.readline, ""))
        return results

if __name__ == '__main__':
    service = KnpService()
    print([mrph.midasi for mrph in service.parse("今日はいい天気ですね").mrph_list()])

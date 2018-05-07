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

class KnpApi(object):
    __knp = KNP()
    MARK_EOS = "EOS"
    @staticmethod
    def parse(string):
        formatted_string = JumanKnpUtil.format_string(string)
        return KnpApi.__knp.parse(formatted_string)
    @staticmethod
    def parse_all(strings):
        return [KnpApi.parse(string) for string in strings.split("\n")]
    @staticmethod
    def result(string_iterator):
        results = []
        data = ""
        for line in string_iterator:
            data += line
            if line.strip() == KnpApi.MARK_EOS:
                results.append(KnpApi.__knp.result(data))
                data=""
        return results
    @staticmethod
    def load_with_handler(string_iterator, handler):
        data = ""
        for line in string_iterator:
            data += line
            if line.strip() == KnpApi.MARK_EOS:
                # 応急処置 (出力がまともに出ていない or 文が長すぎるなどが原因で格解析ができなくて構文解析だけが行われた場合をスキップ)
                if not(JumanKnpUtil.is_match_partly(r"\n\* \d+ ", data)) and not(JumanKnpUtil.is_match_partly(r"Fell back to", data)):
                    handler(KnpApi.__knp.result(data))
                data=""
        return
    @staticmethod
    def load_from_file_with_handler(filepath, handler):
        with open(filepath, "r") as f:
            results = KnpApi.load_with_handler(iter(f.readline, ""), handler)
        return results
    @staticmethod
    def load_from_file(filepath):
        with open(filepath, "r") as f:
            results = KnpApi.result(iter(f.readline, ""))
        return results

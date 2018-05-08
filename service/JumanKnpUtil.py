#coding: utf-8

try:
    import mojimoji
except Exception as e:
    import unicodedata
import re

class RepnameExtractor():
    def __init__(self, options = GetRepnameOptions()):
        self.options = options
    def extract_from_fstring(self, fstring):
        match = re.search(r"代表表記:(.+?)>", fstring)
        if match is not None:
            return match.group(1).split("?")[0]
        return None
    def extract_from_tag(self, tag):
        repname = ""
        # タグの内容語の代表表記
        match = re.search(r"\<正規化代表表記:(.+?)\>", tag.fstring)
        if match is not None:
            repname = match.group(1)
        else:
            match = re.search(r"\<用言代表表記:(.+?)\>", tag.fstring)
            if match is not None:
                repname = match.group(1)
        if self.options.num_normalize:
            # 未実装
            pass
        return repname
    def extract_from_mrph(self, mrph):
        if not(JumanKnpUtil.is_match_partly("<準?内容語>", mrph.fstring)):
            return ""
        if JumanKnpUtil.is_match_partly("<特殊非見出語>", mrph.fstring):# 「後」など
            return ""
        match = re.search(r"<代表表記変更:(.+?)>", mrph.fstring)
        if self.options.pos_change and (match is not None):
            return match.group(1)
        if self.options.num_normalize and mrph.bunrui == "数詞" and not(JumanKnpUtil.is_match_partly(r"^(?:何|幾)$", mrph.midasi)):
            return "[数詞]"
        match2 = re.search(r"<代表表記:(.+?)>", mrph.fstring)
        if self.options.use_disambiguated_repname and (JumanKnpUtil.is_match_partly(r"<(?:用言|名詞)曖昧性解消>", mrph.fstring)) and (match2 is not None):
            return match2.group(1)
        match3 = re.search(r"<正規化代表表記:(.+?)>", mrph.fstring)
        if match3 is not None:
            return match3.group(1)
        return ""
    def extract_from_mlist(self, mlist):
        # 形態素列から代表表記を得る(数詞を汎下するためなどに利用)
        reps = []
        if self.options.head:
            # 主辞代表表記
            for mrph in reversed(mlist):
                rep = self.extract_from_mrph(mrph)
                if rep == "":
                    continue
                # 数詞が連続しないように
                if (rep == "[数詞]") and len(reps) > 0 and reps[-1] == "[数詞]":
                    continue
                reps.append(rep)
                if JumanKnpUtil.is_match_partly(r"<内容語>", mrph.fstring) and not(JumanKnpUtil.is_match_partly(r"^[一-龥]$", mrph.midasi)):
                    break
            reps.reverse()
        else:
            for mrph in mlist:
                rep = self.extract_from_mrph(mrph)
                if rep == "":
                    continue
                if (rep == "[数詞]") and len(reps) > 0 and reps[-1] == "[数詞]":
                    continue
                reps.append(rep)
        return "+".join(reps)
    def extract_from_bnst(self, bnst):
        repname = ""
        mlist = bnst.mrph_list()
        if self.options.pos_change:
            opt = GetRepnameOptions()
            opt.pos_change = True
            extractor = RepnameExtractor(opt)
            repname = extractor.extract_from_mlist(mlist)
        elif self.options.use_disambiguated_repname or self.options.head:
            opt = GetRepnameOptions()
            opt.use_disambiguated_repname = opt.use_disambiguated_repname or self.options.use_disambiguated_repname
            if self.options.head:
                opt.head = True
                opt.num_normalize = True
            extractor = RepnameExtractor(opt)
            repname = extractor.extract_from_mlist(mlist)
        else:
            match = JumanKnpUtil.get_value_from_fstring("正規化代表表記", bnst.fstring)
            if match is not None:
                repname = match
        # 薄くする, 大切にする
        if len(mlist) >= 2 and mlist[0].hinsi == '形容詞' and mlist[1].hinsi == '接尾辞':
            match = re.search(r"^(する|なる)$", mlist[1].genkei)
            if match is not None:
                repname += "+{0}/{0}".format(match.group(1))
        # 子供にくっつけるものがあるかどうかチェック
        if self.options.child_check:
            if repname == "する/する" or repname == "行う/おこなう":
                child_repname = ""
                child_repname_before_change = ""
                for child in bnst.children:
                    child_repname = self.extract_from_bnst(child)
                    # サ変
                    if JumanKnpUtil.is_match_partly(r"<ヲ>", child.fstring) and JumanKnpUtil.is_match_partly(r"<サ変>", child.fstring):
                        child.skip = True
                        return child_repname
                    if JumanKnpUtil.is_match_partly(r"<[ヲニ]>", child.fstring) and JumanKnpUtil.is_meishika(child_repname):
                        # 連用形名詞化 (例: 仕分けをする, 千切りにする)
                        child.skip = True
                        opt = GetRepnameOptions()
                        opt.pos_change = True
                        extractor = RepnameExtractor(opt)
                        child_repname_before_change = extractor.extract_from_bnst(child)
                        return child_repname_before_change
                # 副詞 + する は副詞を述語にくっつける
                # 例:) ゆっくりする
                for child in bnst.children:
                    if JumanKnpUtil.is_match_partly(r"<副詞>", child.fstring) and child.bnst_id == (bnst.bnst_id - 1):
                        # perlではget_repname_from_tagを使っているけどバグでは？
                        extractor = RepnameExtractor()
                        repname = "{}+{}".format(extractor.extract_from_bnst(child), repname)
                        child.skip = True
        return repname

class GetRepnameOptions(object):
    def __init__(self):
        self.child_check = False
        self.use_disambiguated_repname = False
        self.head = False
        self.pos_change = False
        self.num_normalize = False
    def setup(self, opt):
        self.use_disambiguated_repname = opt.use_disambiguated_repname

class GetChildOptions(object):
    def __init__(self):
        self.include_case_analysis = False
        self.use_disambiguated_repname = False
        self.not_extract_ne = False
        self.not_extract_head_in_ne = False
    def setup(self, opt):
        self.use_disambiguated_repname = opt.use_disambiguated_repname
        self.include_case_analysis = opt.include_case_analysis
        self.not_extract_ne = opt.not_extract_ne
        self.not_extract_head_in_ne = opt.not_extract_head_in_ne

class JumanKnpUtil(object):
    PARENT_NONE = -1
    @staticmethod
    def format_input_string(string):
        if mojimoji is not None:
            return mojimoji.han_to_zen(string.replace("\n", ""))
        else:
            return unicodedata.normalize('NFKC', string.replace("\n", ""))
    @staticmethod
    def parse_case_result(params):
        # paramsから、格解析結果を辞書として抽出
        d={}
        for param in params:
            if "格解析結果" in param:
                for p in param.strip("格解析結果:").rsplit(":", 1)[1].split(";"):
                    data = p.split("/")
                    d[data[0]] = data[1:]
        return d
    @staticmethod
    def get_midasi_from_tag(tag):
        return "".join([mrph.midasi for mrph in tag.mrph_list()])
    @staticmethod
    def get_midasi_from_bnst(bnst):
        return "".join([mrph.midasi for mrph in bnst.mrph_list()])
    @staticmethod
    def get_midasi_from_result(result):
        return "".join([JumanKnpUtil.get_midasi_from_bnst(bnst) for bnst in result.bnst_list()])
    @staticmethod
    def get_list_from_fstring(fstring):
        return [f for f in fstring.strip("<>").split("><")]
    @staticmethod
    def is_meishika(repname):
        # 代表表記が名詞化されているかどうか
        # 一番後ろの形態素の代表表記が「v」かどうかを調べる
        last_repname = repname.split("+")[-1]
        for rep in last_repname.split("?"):
            if JumanKnpUtil.is_match_partly(r"v$", rep):
                return True
        return False
    @staticmethod
    def is_youtaihenka(bnst):
        return JumanKnpUtil.is_match_partly(r"<用体変化>", bnst.fstring)
    @staticmethod
    def get_value_from_fstring(key, fstring):
        match = re.search(r"<{0}:(.+?)>".format(key), fstring)
        if match is None:
            return None
        else:
            return match.group(1)
    @staticmethod
    def get_relation_from_fstring(fstring):
        match = re.search(r"<節機能-(.+?)>", fstring)
        if match is not None:
            return match.group(1)
        return None
    @staticmethod
    def get_case_from_fstring(fstring):
        match = re.search(r"<係:([^>]+?)格>", fstring)
        if match is not None:
            return match.group(1)
        return None
    @staticmethod
    def get_cfid_from_fstring(fstring):
        match = re.search(r"<格解析結果:([^:]+?):([^:]+?)[:>]", fstring)
        if match is not None:
            verb = match.group(1)
            cfid = match.group(2)
            return "${}:{}".format(verb, cfid)
        return None
    @staticmethod
    def get_voice_from_fstring(fstring):
        # <態:使役>
        voice = JumanKnpUtil.get_value_from_fstring("態", fstring)
        if voice is not None:
            return re.sub(r'\|', "│", voice)
        else:
            return None
    @staticmethod
    def get_relation_main(relationString):
        if relationString is not None:
            return relationString.split(";")[0]
        else:
            return None
    @staticmethod
    def is_match_partly(pattern, string):
        if re.search(pattern, string) is not None:
            return True
        return False
    @staticmethod
    def get_last_mrph(bnst):
        # 記号を除いた一番後ろの形態素
        mrph_list = bnst.mrph_list()
        last_mrph = mrph_list[-1]
        if len(mrph_list) > 1 and JumanKnpUtil.is_symbol_mrph(last_mrph):
            return bnst.mrph_list()[-2]
        else:
            return last_mrph
    @staticmethod
    def is_symbol_mrph(mrph):
        bunrui = mrph.bunrui
        if bunrui == "記号" or bunrui == "空白" or bunrui == "読点":
            return True
        return False

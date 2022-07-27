# coding=utf-8
import sys
import javalang
sys.path.append('..')
from lexical_analysis.TestLexer import TestLexer
from lexical_analysis.TypeUtil import TypeUtil


class findImports(TypeUtil):
    buffer = ''
    i = 0
    ch = ' '
    strToken = ''
    import_paths = []
    tokenize = []
    modified = False

    def __init__(self, string):
        self.modified = False
        # format_annotation内部会修改self.modified
        self.buffer = string
        self.i = 0
        self.ch = ' '
        self.strToken = ''
        self.import_paths = []
        self.tokenize = []
        try:
            self.init_tokens()
        except:
            self.buffer = self.format_annotation(string)
            self.init_tokens(ignore_errors=True)

    def init_tokens(self, ignore_errors=False):
        self.tokenize = []
        tokens = list(javalang.tokenizer.tokenize(self.buffer, ignore_errors=ignore_errors))
        for token in tokens:
            self.tokenize.append(token.value)

    def find_java_imports(self):
        self.strToken = ''

        while self.i < len(self.tokenize):
            if not self.nextToken():
                break
            if self.strToken in ['class']:#, 'public']:  # 不考虑import之后的内容
                break
            if self.strToken == 'import':  #
                path = ''
                if not self.nextToken():
                    break
                while self.i < len(self.buffer) and self.strToken != ';':
                    path += self.strToken
                    if not self.nextToken():
                        break
                self.import_paths.append(path)
        return self.import_paths

    def nextToken(self):
        self.i += 1
        if self.i >= len(self.tokenize):
            return False
        else:
            self.strToken = self.tokenize[self.i]
            return True

    def filter_key_words(self, classes):
        classes_new = []
        for word in classes:
            if word not in self.keyWords:
                classes_new.append(word)
        return classes_new

    # 在调用javalang进行解析抛出异常后，则直接基于词法分析的方法，将词法分析中除分隔符以外的单词，去掉与操作符相邻的的ident作为候选的类名
    def get_class_error(self):
        classes = []
        # print(self.tokenize[self.i:])
        # 最后一个不可能是类名，为了防止数组越界，这里减去1
        while self.i < len(self.tokenize)-1:
            if self.tokenize[self.i] not in self.operators and self.tokenize[self.i] not in self.separators:
                # 下一个是括号，或者下一个不是运算符等，才认为其可能是类名
                if (self.tokenize[self.i + 1] in ['{', '(', '[', '<']) or (self.tokenize[self.i + 1] not in self.operators and self.tokenize[self.i + 1] not in self.separators):
                    classes.append(self.tokenize[self.i])
            self.i += 1
        return classes

    def get_idents_except_import(self):
        classes = []
        try:
            tree = javalang.parse.parse(self.buffer)
            for type in tree.types:
                type_string = str(type)
                for i in range(len(type_string)):
                    if type_string[i:i + len('ReferenceType')] == 'ReferenceType':
                        string = self.get_str_referenceType(type_string, i)
                        class_name = self.find_name_from_ReferenceType(string)
                        classes.append(class_name.split('.')[0])
                    elif type_string[i:i+len('MemberReference')] == 'MemberReference':
                        string = self.get_str_referenceType(type_string, i)
                        class_name = self.find_name_from_MemberReference(string)
                        if class_name != '' and class_name != 'None':
                            classes.append(class_name.split('.')[0])
        except Exception as e:
            classes = self.get_class_error()
        classes = self.filter_key_words(classes)
        for file in self.import_paths:
            idents_remove = file.split('.')[-1]
            if idents_remove in classes:
                classes.remove(idents_remove)
        return classes

    # 寻找类似ReferenceType(arguments=None, dimensions=[], name=String, sub_type=None)的字符串
    def get_str_referenceType(self, type_string, i):
        count_left = 0
        found_left = False
        j = i-1
        while j+1 < len(type_string):
            j += 1
            if type_string[j] == '(':
                found_left = True
                count_left += 1
            elif type_string[j] == ')':
                count_left -= 1
                if found_left and count_left == 0:
                    break

        return type_string[i: j+1]

    # 获取ReferenceType(arguments=None, dimensions=[], name=String, sub_type=None)的name字段
    def find_name_from_ReferenceType(self, type_string):
        name_start = 0
        name_end = 0
        count_left = 0
        j = -1
        while j + 1 < len(type_string):
            j += 1
            if type_string[j] == '(':
                count_left += 1
            elif type_string[j] == ')':
                count_left -= 1

            if type_string[j: j +len(' name=')] == ' name=' and count_left == 1:
                # print(type_string[j +len(' name=')])
                name_start = j +len(' name=')
                for k in range(j,len(type_string)):
                    if type_string[k] == ',':
                        name_end = k
                        break
                break
        # print(type_string[name_start: name_end])
        return type_string[name_start: name_end]

    # 获取ReferenceType(arguments=None, dimensions=[], name=String, sub_type=None)的name字段
    def find_name_from_MemberReference(self, type_string):
        name_start = 0
        name_end = 0
        count_left = 0
        j = -1
        while j + 1 < len(type_string):
            j += 1
            if type_string[j] == '(':
                count_left += 1
            elif type_string[j] == ')':
                count_left -= 1

            if type_string[j: j +len(' qualifier=')] == ' qualifier=' and count_left == 1:
                # print(type_string[j +len(' name=')])
                name_start = j +len(' qualifier=')
                for k in range(j,len(type_string)):
                    if type_string[k] == ',':
                        name_end = k
                        break
                break
        # print(type_string[name_start: name_end])
        return type_string[name_start: name_end]

    # 部分java文件出现注释中嵌套注释，导致词法分析出错
    def format_annotation(self, string):

        # 先统计
        last_right = -1
        # 当前的注释左右边界数量，如右边界数量>=2,则倒数第二个*/改为_/

        i = 0
        while i<len(string)-1:
            if string[i] == '"':
                found = False
                need_replace = []
                while i < len(string) - 1:
                    i += 1
                    # if string[i:i + 2] == '*/' or string[i:i + 2] == '/*':
                    #     need_replace.append(i)
                    if string[i] == '"' or string[i] == '\n':
                        found = True
                        break
                if found:
                    # for need in need_replace:
                    #     self.modified = True
                    #     string = string[:need] + '__' + string[need+2:]
                    pass
            elif string[i:i+2] == '//':
                i += 1
                while i<len(string)-1:
                    i += 1
                    if string[i] == '\n':
                        break
            # 出现了错误的右边界，认为上一个右边界有问题，但若这是第一次出现*/,则认为这个右边界不应该出现，进行替换
            elif string[i:i+2] == '*/':
                # print(i)
                self.modified = True
                if last_right == -1:
                    string = string[:i] + '__' + string[i+2:]
                else:
                    string = string[:last_right] + '__' + string[last_right+2:]
                    last_right = i
                i += 1
            elif string[i:i+2] == '/*':
                found = False
                i += 1
                while i<len(string)-1:
                    i += 1
                    #if string[i] == '"':
                    #    need_replace = []
                    #    found_ = False
                    #    while i < len(string) - 1:
                    #        i += 1
                    #        if string[i:i + 2] == '*/' or string[i:i + 2] == '/*':
                    #            need_replace.append(i)
                    #        if string[i] == '"':
                    #            found_ = True
                    #            break
                    #    if found_:
                    #        for need in need_replace:
                    #            self.modified = True
                    #            string = string[:need] + '__' + string[need + 2:]
                    if string[i:i+2] == '*/':
                        last_right = i
                        found = True
                        break
                if not found:
                    string += '*/'
                else:
                    i += 1
            i+=1
        return string

    def get_modified(self):
        return self.modified
# coding=utf-8
from .TypeUtil import TypeUtil
from .FileUtil import FileUtil
'''
 * 词法分析
 * 关键字，运算符一符一类
 * 标识符，常数，分隔符各自一类
 * 运算符未处理组合运算 ++、--、+= 等
'''


class TestLexer(TypeUtil):
    buffer = ''
    i = 0
    ch = ' '
    strToken = ''
    '''
     * 读取指定路径文件
     * @param fileSrc 读取文件路径
    '''
    def __init__(self, string):
        self.buffer = string
        self.i = 0
        self.ch = ' '
        self.strToken = ''
        # self.buffer, success = FileUtil.readFile(file_in);

    '''
     * 词法分析
    '''
    def analyse(self, include_ann=False):
        resultString = []
        self.strToken = ''  # 置strToken为空串

        while self.i < len(self.buffer):
            self.getChar()
            self.getBC()
            if self.isLetter(self.ch):  # 如果ch为字母
                while self.isLetter(self.ch) or self.isDigit(self.ch):
                    self.concat()
                    self.getChar()
                self.retract()  # 回调
                if self.isKeyWord(self.strToken):
                    pass
                else:
                    resultString.append(self.strToken)
                self.strToken = ''
            elif self.isDigit(self.ch): # 不考虑小数
                while self.isDigit(self.ch):    # ch为数字
                    self.concat()
                    self.getChar()
                if not self.isLetter(self.ch):  # 不能数字+字母
                    self.retract()  # 回调
                    resultString.append(self.strToken)
                else:
                    pass
                self.strToken = ''
            elif self.isOperator(self.ch):  # 运算符
                if self.ch == '/':
                    self.getChar()
                    if include_ann:
                        if self.ch == '*':   # 为/*注释
                            while self.i < len(self.buffer):
                                self.getChar()
                                if self.ch == '*': # 可能为*/表示注释结束
                                    self.getChar()
                                    if self.ch == '/':  # 为*/表示注释结束
                                        self.getChar()
                                        break
                    if self.ch == '/':  # //为单行注释
                        if include_ann:
                            while not self.ch == '\n':
                                self.getChar()
                        self.getChar()
                    self.retract()
                elif self.ch == '+':
                    pass
                elif self.ch == '-':
                    pass
                elif self.ch == '*':
                    pass
                elif self.ch == '/':
                    pass
                elif self.ch == '>':
                    pass
                elif self.ch == '<':
                    pass
                elif self.ch == '=':
                    pass
                elif self.ch == '&':
                    pass
                elif self.ch == '|':
                    pass
                elif self.ch == '~':
                    pass
                else:
                    pass
            elif self.isSeparators(self.ch):
                pass
            elif self.ch == '\n':
                continue
            else:
                continue
        return resultString

    '''
     * 将下一个输入字符读到ch中，搜索指示器前移一个字符
    '''
    def getChar(self):
        self.ch = self.buffer[self.i]
        self.i += 1

    '''
     * 检查ch中的字符是否为空白，若是则调用getChar()直至ch中进入一个非空白字符*/
    '''
    def getBC(self):
        # isSpaceChar(char ch) 确定指定字符是否为 Unicode 空白字符。
        # 上述方法不能识别换行符
        self.ch = str(self.ch)
        while self.ch.isspace() and self.i < len(self.buffer):
            self.getChar()

    # 将ch连接到strToken之后
    def concat(self):
        self.strToken += self.ch

    # 将搜索指示器回调一个字符位置，将ch值为空白字
    def retract(self):
        self.i -= 1
        self.ch = ''


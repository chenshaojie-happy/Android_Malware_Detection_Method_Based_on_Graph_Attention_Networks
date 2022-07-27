# coding=utf-8


class TypeUtil:

    keyWords = ["abstract", "boolean", "break", "byte",
        "case", "catch", "char", "class", "continue", "default", "do",
        "double", "else", "extends", "final", "finally", "float", "for",
        "if", "implements", "import", "instanceof", "int", "interface",
        "long", "native", "new", "package", "private", "protected",
        "public", "return", "short", "static", "super", "switch",
        "synchronized", "this", "throw", "throws", "transient", "try",
        "void", "volatile", "while", "strictfp", "enum", "goto", "const", "assert"] # 关键字数组
    operators = ['+', '-', '*', '/', '=', '>', '<', '&', '|','!']; # 运算符数组
    separators = [',', ';', '{', '}', '(', ')', '[', ']', '_', ':', '.', '"', '\\'] # 界符数组

    '''
    * 判断是否为字母
    * @ param ch 需判断的字符
    * @
    
    
    return boolean
    '''
    def isLetter(self, ch):
        ch = str(ch)
        if '\u4e00' <= ch <= '\u9fff':
            return True
        return ch.isalpha()


    '''
    *判断是否为数字
     * @ param
    ch
    需判断的字符
    * @
    return boolean
    '''
    def isDigit(self, ch):
        ch = str(ch)
        return ch.isdigit()

    '''
    *判断是否为关键字
     * @ param
    s
    需判断的字符串
    * @
    return boolean
    '''
    def isKeyWord(self, string):
        string = str(string)
        for i in range(len(self.keyWords)):
            if string == self.keyWords[i]:
                return True
        return False

    '''
    *判断是否为运算符
     * @ param
    ch
    需判断的字符
    * @
    return boolean
    '''
    def isOperator(self, ch):
        ch = str(ch)
        for i in range(len(self.operators)):
            if ch == self.operators[i]:
                return True
        return False

    '''
    *判断是否为分隔符
     * @ param
    ch
    需判断的字符
    * @
    return boolean
    '''

    def isSeparators(self, ch):
        ch = str(ch)
        for i in range(len(self.separators)):
            if ch == self.separators[i]:
                return True
        return False


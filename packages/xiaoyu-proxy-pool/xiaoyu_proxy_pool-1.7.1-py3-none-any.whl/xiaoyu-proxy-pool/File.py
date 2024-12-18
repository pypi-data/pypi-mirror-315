import string
class File_Filenew_text:
    def Pawword_Text(password):
    # 弱密码：长度小于6，或者只包含字母
        if len(password) < 6 or all(char in string.ascii_letters for char in password):
            return "弱密码"
        # 中等密码：长度在6到8之间，包含字母和数字
        elif 6 <= len(password) < 8 and any(char.isdigit() for char in password):
            return "中等密码"
        # 强密码：长度大于等于8，包含字母、数字和标点符号
        elif len(password) >= 8 and any(char.isdigit() for char in password) and any(char in string.punctuation for char in password):
            return "强密码"
        else:
            return "密码强度未知"


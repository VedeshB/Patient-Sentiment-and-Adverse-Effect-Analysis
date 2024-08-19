import string
def filter_word(n):
    print(n, 'input')
    res = []
    for i in [n]:
        t, st = [], ''
        for j in i:
            if j in string.punctuation or j.isspace():
                if not st.strip().isspace():
                    t.append(st.strip())
                st = ''
            else:
                st += j
        t.append(st.strip())
        res.append('-'.join(list(filter(lambda x: x != '', t))))
    return res

def t_ex(text):
        text2 = []
        s = ''
        for i in text:
            if i != '.':
                s += i
            elif i == '.':
                text2.append(s)
                s = ''
        if s:
            text2.append(s)
        return text2
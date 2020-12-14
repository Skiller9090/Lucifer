def check_int(s):
    if s.count(".") == 1:
        if not (s.split(".")[1].count("0") == len(s.split(".")[1])):
            return False
        return check_int_quick(s.split(".")[0])
    if s.count(".") > 1:
        return False
    return check_int_quick(s)


def check_int_quick(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

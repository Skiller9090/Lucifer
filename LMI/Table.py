from termcolor import colored

from LMI import Reports


def generate_table(array2d, title="", headings=None):
    if headings is not None:
        array2d.insert(0, headings)
    if Reports.isReporting:
        Reports.HTMLReport.addTable((title, array2d))
    out = ""
    max_char = -1
    max_cols = -1
    a_title, b_title, max_char, max_cols = calculate_formatting(array2d, max_char, max_cols, title)
    dash_column = "—" * max_char
    out = generate_title(a_title, b_title, dash_column, max_char, max_cols, out, title)
    for i, line in enumerate(array2d):
        while len(line) < max_cols:
            line.append("")
        out = generate_row(array2d, dash_column, headings, i, line, max_char, max_cols, out)
    out += f'└{"┴".join(([dash_column] * max_cols))}┘\n'
    return out


def generate_row(array2d, dash_column, headings, i, line, max_char, max_cols, out):
    depth = 1
    dataCells = []
    for data in line:
        data = str(data)
        nl_count = data.count("\n") + 1
        depth = nl_count if nl_count > depth else depth
        dataCells.append(data.split("\n"))
    for v in dataCells:
        while len(v) < depth:
            v.append("")
    for c, cellsLine in enumerate(zip(*dataCells)):
        out += "│" if c == 0 else "\n│"
        for cell in cellsLine:
            total = max_char - len(str(cell))
            before, after = total // 2, total - (total // 2)
            if headings is not None and i == 0:
                cell = colored(cell, "blue", attrs=[])
            out += f"{' ' * before}{cell}{' ' * after}│"
    out += f'\n├{"┼".join(([dash_column] * max_cols))}┤\n' \
        if i != len(array2d) - 1 else "\n"
    return out


def calculate_formatting(array2d, max_char, max_cols, title):
    for line in array2d:
        max_cols = max(len(line), max_cols)
        for cell in line:
            cellLines = str(cell).split("\n")
            for string in cellLines:
                max_char = max(len(str(string)), max_char)
    title_total = (max_char * max_cols) + (max_cols - 1) - len(str(title))
    if title_total < 0:
        max_char = int(round(len(str(title)) / max_cols))
        title_total = (max_char * max_cols) + (max_cols - 1) - len(str(title))
    b_title, a_title = title_total // 2, title_total - (title_total // 2)
    return a_title, b_title, max_char, max_cols


def generate_title(a_title, b_title, dash_column, max_char, max_cols, out, title):
    if title != "":
        out += f'┌{"—" * ((max_char * max_cols) + (max_cols - 1))}┐\n'
        out += f'│{" " * b_title}{colored(title, "green", attrs=["bold"])}{" " * a_title}│\n'
        out += f'├{"┬".join(([dash_column] * max_cols))}┤\n'
    else:
        out += f'┌{"┬".join(([dash_column] * max_cols))}┐\n'
    return out


def dictionary_max_transformation(dictionary, max_chars=30):
    to_transform = dictionary.copy()
    for k, v in zip(to_transform.keys(), to_transform.values()):
        eachPiece = v.split("\n")
        new_set = []
        for q in eachPiece:
            split_cell, temp = get_max_char_line(max_chars, q)
            split_cell.append(" ".join(temp))
            new_set.append("\n".join(split_cell))
        to_transform[k] = "\n".join(new_set).strip("\n")
    return to_transform


def get_max_char_line(max_chars, q):
    current = 0
    words = q.split(" ")
    split_cell = []
    temp = []
    for word in words:
        current += len(word)
        if current >= max_chars:
            split_cell.append(" ".join(temp))
            temp = [word]
            current = len(word)
        else:
            temp.append(word)
    return split_cell, temp
